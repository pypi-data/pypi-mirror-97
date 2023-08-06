from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd
from pydantic import BaseModel

from xlavir.util import find_file_for_each_sample

SAMPLE_NAME_CLEANUP = [
    '.genome.per-base.bed.gz',
    '.per-base.bed.gz',
    '.trim',
    '.mkD',
]

GLOB_PATTERNS = [
    '**/mosdepth/**/*.genome.per-base.bed.gz',
    '**/mosdepth/**/*.per-base.bed.gz'
]


class MosdepthDepthInfo(BaseModel):
    sample: str
    n_zero_coverage: int
    zero_coverage_coords: str
    low_coverage_threshold: int = 5
    n_low_coverage: int
    low_coverage_coords: str
    genome_coverage: float
    mean_coverage: float
    median_coverage: int


def read_mosdepth_bed(p: Path) -> pd.DataFrame:
    return pd.read_table(p, header=None, names=['genome', 'start_idx', 'end_idx', 'depth'])


def get_interval_coords_bed(df: pd.DataFrame, threshold: int = 0) -> str:
    df_below = df[df.depth <= threshold]
    start_pos, end_pos = df_below.start_idx, df_below.end_idx
    coords = []
    for x, y in zip(start_pos, end_pos):
        if coords:
            last = coords[-1][-1]
            if x == last + 1:
                coords[-1].append(x)
                coords[-1].append(y - 1)
            else:
                coords.append([x, y - 1])
        else:
            coords.append([x, y - 1])
    return '; '.join([f'{xs[0] + 1}-{xs[-1] + 1}' if xs[0] != xs[-1] else f'{xs[0]}' for xs in coords])


def count_positions(df: pd.DataFrame) -> int:
    return (df.end_idx - df.start_idx).sum()


def get_genome_coverage(df: pd.DataFrame, low_coverage_threshold: int = 5) -> float:
    genome_length = df.end_idx.max()
    return 1.0 - (count_positions(df[df.depth < low_coverage_threshold]) / genome_length)


def depth_array(df: pd.DataFrame) -> np.ndarray:
    arr = np.zeros(df.end_idx.max())
    for row in df.itertuples():
        arr[row.start_idx:row.end_idx] = row.depth
    return arr


def get_info(basedir: Path, low_coverage_threshold: int = 5) -> Dict[str, MosdepthDepthInfo]:
    sample_beds = find_file_for_each_sample(basedir,
                                            glob_patterns=GLOB_PATTERNS,
                                            sample_name_cleanup=SAMPLE_NAME_CLEANUP)
    out = {}
    for sample, bed_path in sample_beds.items():
        df = read_mosdepth_bed(bed_path)
        arr = depth_array(df)
        mean_cov = arr.mean()
        median_cov = pd.Series(arr).median()
        depth_info = MosdepthDepthInfo(sample=sample,
                                       low_coverage_threshold=low_coverage_threshold,
                                       n_low_coverage=count_positions(df[df.depth < low_coverage_threshold]),
                                       n_zero_coverage=count_positions(df[df.depth == 0]),
                                       zero_coverage_coords=get_interval_coords_bed(df),
                                       low_coverage_coords=get_interval_coords_bed(df, low_coverage_threshold),
                                       genome_coverage=get_genome_coverage(df, low_coverage_threshold),
                                       mean_coverage=mean_cov,
                                       median_coverage=median_cov)
        out[sample] = depth_info
    return out
