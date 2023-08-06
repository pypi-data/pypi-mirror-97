import logging
import os
import re
from enum import Enum
from operator import itemgetter
from pathlib import Path
from typing import Dict, Tuple, List, Optional, Iterable

import pandas as pd
from pydantic import BaseModel

from xlavir.util import try_parse_number, find_file_for_each_sample

logger = logging.getLogger(__name__)

aa_codes = dict(
    ALA='A',
    ARG='R',
    ASN='N',
    ASP='D',
    CYS='C',
    GLU='E',
    GLN='Q',
    GLY='G',
    HIS='H',
    ILE='I',
    LEU='L',
    LYS='K',
    MET='M',
    PHE='F',
    PRO='P',
    SER='S',
    THR='T',
    TRP='W',
    TYR='Y',
    VAL='V',
    TER='*',
)

# list of tuples: [0]: column id; [1]: report column id/name; [2]: column description for report cell comment
variants_cols = [
    ('sample', 'Sample', 'Sample name',),
    ('CHROM', 'Reference Genome', 'Reference genome sequence ID/name'),
    (
        'mutation',
        'Mutation',
        'Mutation found in sample with format '
        '"{reference allele}{reference position}{allele in sample}"'
        ' with predicted amino acid change information in brackets with format '
        '"{gene name}:{reference AA}{gene AA position}{AA change}"'
    ),
    ('POS', 'Position', '1-based nucleotide position in reference sequence'),
    ('REF', 'Reference Allele', 'Nucleotide allele sequence found in reference sequence'),
    ('ALT', 'Alternate Allele', 'Nucleotide allele sequence found in sample'),
    (
        'REF_DP',
        'Reference Allele Depth',
        'Read depth of coverage supporting reference allele at reference position'
    ),
    (
        'ALT_DP',
        'Alternate Allele Depth',
        'Read depth of coverage supporting alternate allele at reference position',
    ),
    ('DP', 'Total Depth', 'Total depth of coverage at reference position',),
    (
        'ALT_FREQ',
        'Alternate Allele Frequency',
        'Observed frequency of alternate allele variant',
    ),
    ('gene', 'Gene', 'Gene name',),
    (
        'impact',
        'Variant Impact',
        'SnpEff estimation of putative impact or deleteriousness of variant '
        '(see https://pcingola.github.io/SnpEff/se_inputoutput/#ann-field-vcf-output-files)'
    ),
    (
        'effect',
        'Variant Effect',
        'Effect of variant annotated using Sequence Ontology terms, e.g.'
        'for "missense_variant", see http://www.sequenceontology.org/browser/current_release/term/SO:0001583'
        ' where the definition is "A sequence variant, that changes one or more bases, resulting in a '
        'different amino acid sequence but where the length is preserved."'
    ),
    ('aa', 'Amino Acid Change', 'The change in the sample\'s gene amino acid sequence'
                                ' relative to the reference sequence'),
    ('aa_pos', 'Amino Acid Position', 'Position of amino acid change in the reference sequence gene'),
    ('aa_len', 'Gene Amino Acid Length', 'Amino acid length of the reference sequence gene'),
]

BCFTOOLS_STATS_GLOB_PATTERNS = [
    '**/ivar/**/*AF0.*.bcftools_stats.txt',
    '**/ivar/**/*.bcftools_stats.txt',
    '**/*AF0.*.bcftools_stats.txt',
    '**/*.bcftools_stats.txt',
]

BCFTOOLS_STATS_SAMPLE_NAME_CLEANUP = [
    re.compile(r'\.AF0\.\d+\.bcftools_stats.txt$')
]


class VariantStats(BaseModel):
    sample: str
    n_snp: int
    n_mnp: int
    n_indel: int


class VariantCaller(Enum):
    iVar = 'iVar'
    Longshot = 'Longshot'


VCF_GLOB_PATTERNS = [
    '**/ivar/*.vcf.gz',
    '**/*.vcf',
]

VCF_SAMPLE_NAME_CLEANUP = [
    re.compile(r'\.vcf(\.gz)?$'),
    re.compile(r'\.AF0\.\d+(\.filt)?'),
    re.compile(r'\.0\.\d+AF(\.filt)?'),
]

SNPSIFT_GLOB_PATTERNS = [
    '**/ivar/**/*.snpSift.table.txt',
    '**/*.snpSift.table.txt',
]

SNPSIFT_SAMPLE_NAME_CLEANUP = [
    re.compile(r'\.snpSift\.table\.txt$'),
    re.compile(r'\.AF0\.\d+(\.filt)?'),
    re.compile(r'\.0\.\d+AF(\.filt)?'),
]


def vcf_selector(paths: List[Path]) -> Optional[Path]:
    xs = []
    for path in paths:
        variant_caller, df = read_vcf(path)
        xs.append((df.shape[0], path))
    xs.sort(reverse=True)
    try:
        return xs[0][1]
    except KeyError:
        return None


def snpsift_selector(paths: List[Path]) -> Optional[Path]:
    xs = []
    for path in paths:
        df = pd.read_table(path)
        xs.append((df.shape[0], path))
    xs.sort(reverse=True)
    try:
        return xs[0][1]
    except KeyError:
        return None


def read_vcf(vcf_file: Path) -> Tuple[str, pd.DataFrame]:
    """Read VCF file into a DataFrame"""
    gzipped = vcf_file.name.endswith('.gz')
    with os.popen(f'zcat < {vcf_file.absolute()}') if gzipped else open(vcf_file) as fh:
        vcf_cols = []
        variant_caller = ''
        for line in fh:
            if line.startswith('##source='):
                variant_caller = line.strip().replace('##source=', '')
            if line.startswith('#CHROM'):
                vcf_cols = line[1:].strip().split('\t')
                break
        df = pd.read_table(fh,
                           comment='#',
                           header=None,
                           names=vcf_cols)
    return variant_caller, df


def parse_aa(gene: str,
             ref: str,
             alt: str,
             nt_pos: int,
             aa_pos: int,
             snpeff_aa: str,
             effect: str) -> str:
    m = re.match(r'p\.([a-zA-Z]+)(\d+)([a-zA-Z]+)', snpeff_aa)
    if snpeff_aa == '.' or m is None:
        return f'{ref}{nt_pos}{alt}'
    ref_aa, aa_pos_str, alt_aa = m.groups()
    ref_aa = get_aa(ref_aa)

    if effect == 'stop_lost':
        alt_aa = get_aa(alt_aa.replace('ext', ''))
        return f'{ref}{nt_pos}{alt}({gene}:{ref_aa}{aa_pos}{alt_aa}[stop_lost])'
    if effect == 'frameshift_variant':
        return f'{ref}{nt_pos}{alt}({gene}:{ref_aa}{aa_pos}[FRAMESHIFT])'
    if effect == 'conservative_inframe_deletion':
        return f'{ref}{nt_pos}{alt}({gene}:{ref_aa}{aa_pos}{alt_aa})'

    alt_aa = get_aa(alt_aa)
    return f'{ref}{nt_pos}{alt}({gene}:{ref_aa}{aa_pos}{alt_aa})'


def get_aa(s: str) -> str:
    out = ''
    for i in range(0, len(s), 3):
        aa = s[i: i + 3]
        aa_code = aa_codes[aa.upper()]
        out += aa_code
    return out


def simplify_snpsift(df: pd.DataFrame, sample_name: str) -> Optional[pd.DataFrame]:
    if df.empty:
        return None
    field_names = set()
    series = []
    for c in df.columns:
        if c == 'AC':
            df_ac = df[c].str.split(',', n=1, expand=True)
            REF_AC = df_ac[0].astype(int)
            REF_AC.name = 'REF_AC'
            ALT_AC = df_ac[1].astype(int)
            ALT_AC.name = 'ALT_AC'
            AF = ALT_AC / (REF_AC + ALT_AC)
            AF.name = 'AF'
            series += [REF_AC, ALT_AC, AF]
            continue
        idx = c.find('[*].')
        if idx > 0:
            new_series_name = c[idx + 4:].lower()
            if new_series_name in field_names:
                continue
            else:
                field_names.add(new_series_name)
            new_series = df[c].str.split(',', n=1, expand=True)[0]
            new_series.name = new_series_name
            series.append(new_series)
        else:
            series.append(df[c])
    df_out = pd.concat(series, axis=1)
    mutation_desc = []
    for row in df_out.itertuples():
        mutation_desc.append(parse_aa(gene=row.gene,
                                      ref=row.REF,
                                      alt=row.ALT,
                                      nt_pos=row.POS,
                                      aa_pos=row.aa_pos,
                                      snpeff_aa=row.aa,
                                      effect=row.effect))

    df_out['mutation'] = mutation_desc
    df_out['sample'] = sample_name
    return df_out


def parse_ivar_vcf(df: pd.DataFrame, sample_name: str = None) -> Optional[pd.DataFrame]:
    if df.empty:
        return None
    if not sample_name:
        sample_name = df.columns[-1] if df.columns[-1] != 'SAMPLE' else None
        if sample_name is None:
            raise ValueError(f'Sample name is not defined for VCF: shape={df.shape}; columns={df.columns}')
    pos_fmt_val = {}
    for row in df.itertuples():
        ks = row.FORMAT.split(':')
        vs = row[-1].split(':')
        pos_fmt_val[row.POS] = {k: try_parse_number(v) for k, v in zip(ks, vs)}
    df_ivar_info = pd.DataFrame(pos_fmt_val).transpose()
    df_ivar_info.index.name = 'POS'
    df_ivar_info.reset_index(inplace=True)
    df_merge = pd.merge(df, df_ivar_info, on='POS')
    df_merge['sample'] = sample_name
    df_merge['DP'] = df_merge.ALT_DP + df_merge.REF_DP
    return df_merge.drop(columns=['ID', 'INFO', 'QUAL', 'FILTER', 'FORMAT', df.columns[-1], 'GT'])


def merge_vcf_snpsift(df_vcf: Optional[pd.DataFrame],
                      df_snpsift: Optional[pd.DataFrame]) -> Optional[pd.DataFrame]:
    if df_snpsift is None and df_vcf is None:
        return None
    if df_vcf is None:
        snpsift_cols = set(df_snpsift.columns)
        return df_snpsift.loc[:, [x for x, _, _ in variants_cols if x in snpsift_cols]]
    if df_snpsift is None:
        vcf_cols = set(df_vcf.columns)
        return df_vcf.loc[:, [x for x, _, _ in variants_cols if x in vcf_cols]]

    df_merge = pd.merge(df_vcf, df_snpsift)
    merged_cols = set(df_merge.columns)
    return df_merge.loc[:, [x for x, _, _ in variants_cols if x in merged_cols]]


def parse_longshot_vcf(df: pd.DataFrame, sample_name: str = None) -> Optional[pd.DataFrame]:
    if df.empty:
        return None
    if not sample_name:
        sample_name = df.columns[-1] if df.columns[-1] != 'SAMPLE' else None
        if sample_name is None:
            raise ValueError(f'Sample name is not defined for VCF: shape={df.shape}; columns={df.columns}')
    pos_info_val = {}
    for row in df.itertuples():
        infos = parse_vcf_info(row.INFO)
        ac_ref, ac_alt = infos['AC']
        infos['REF_DP'] = ac_ref
        infos['ALT_DP'] = ac_alt
        pos_info_val[row.POS] = infos
    df_longshot_info = pd.DataFrame(pos_info_val).transpose()
    df_longshot_info.index.name = 'POS'
    df_longshot_info.reset_index(inplace=True)
    df_merge = pd.merge(df, df_longshot_info, on='POS')
    df_merge['sample'] = sample_name
    df_merge['ALT_FREQ'] = df_merge.ALT_DP / df_merge.DP
    cols_to_keep = list({col for col, _, _ in variants_cols} & set(df_merge.columns))
    return df_merge.loc[:, cols_to_keep]


def parse_vcf_info(s: str) -> dict:
    out = {}
    for x in s.split(';'):
        if not x:
            continue
        key, val_str = x.split('=', maxsplit=1)
        out[key] = try_parse_number(val_str)
    return out


def get_info(basedir: Path) -> Dict[str, pd.DataFrame]:
    sample_vcf = find_file_for_each_sample(basedir=basedir,
                                           glob_patterns=VCF_GLOB_PATTERNS,
                                           sample_name_cleanup=VCF_SAMPLE_NAME_CLEANUP,
                                           single_entry_selector_func=vcf_selector)
    sample_dfvcf = {}
    for sample, vcf_path in sample_vcf.items():
        variant_caller, df_vcf = read_vcf(vcf_path)
        if variant_caller.startswith(VariantCaller.iVar.value):
            df_parsed_ivar_vcf = parse_ivar_vcf(df_vcf, sample)
            if df_parsed_ivar_vcf is not None:
                sample_dfvcf[sample] = df_parsed_ivar_vcf
            else:
                logger.warning(f'Sample "{sample}" has no entries in VCF "{vcf_path}"')
        elif variant_caller.startswith(VariantCaller.Longshot.value):
            df_parsed_ivar_vcf = parse_longshot_vcf(df_vcf, sample)
            if df_parsed_ivar_vcf is not None:
                sample_dfvcf[sample] = df_parsed_ivar_vcf
            else:
                logger.warning(f'Sample "{sample}" has no entries in VCF "{vcf_path}"')
        else:
            raise NotImplementedError()

    sample_snpsift = find_file_for_each_sample(basedir=basedir,
                                               glob_patterns=SNPSIFT_GLOB_PATTERNS,
                                               sample_name_cleanup=SNPSIFT_SAMPLE_NAME_CLEANUP,
                                               single_entry_selector_func=snpsift_selector)
    sample_dfsnpsift = {}
    for sample, snpsift_path in sample_snpsift.items():
        df_snpsift = simplify_snpsift(pd.read_table(snpsift_path), sample)
        if df_snpsift is not None:
            sample_dfsnpsift[sample] = df_snpsift
        else:
            logger.warning(f'Sample "{sample}" has no entries in VCF "{snpsift_path}"')
    out = {}
    set_vcf_samples = set(sample_dfvcf.keys())
    set_snpsift_samples = set(sample_dfsnpsift.keys())
    all_samples = set_vcf_samples | set_snpsift_samples
    logger.debug(f'all_samples={len(all_samples)} | '
                 f'vcf only samples={set_vcf_samples - set_snpsift_samples} |'
                 f'snpsift only samples={set_snpsift_samples - set_vcf_samples}')
    for sample in all_samples:
        df_snpsift = sample_dfsnpsift.get(sample, None)
        df_vcf = sample_dfvcf.get(sample, None)
        df_merged = merge_vcf_snpsift(df_vcf, df_snpsift)
        if df_merged is None:
            continue
        out[sample] = df_merged

    return out


def to_dataframe(dfs: Iterable[pd.DataFrame]) -> pd.DataFrame:
    df = pd.concat(list(dfs))
    df.sort_values(['sample', 'POS'], inplace=True)
    df.set_index('sample', inplace=True)
    df.index.name = 'Sample'
    return df.rename(columns={x: y for x, y, _ in variants_cols})


def to_variant_pivot_table(df: pd.DataFrame) -> pd.DataFrame:
    df_vars = df.copy()
    df_vars.reset_index(inplace=True)
    df_pivot = pd.pivot_table(df_vars,
                              index='Sample',
                              columns='Mutation',
                              values='Alternate Allele Frequency',
                              aggfunc='first',
                              fill_value=0.0)
    pivot_cols = list(zip(df_pivot.columns,
                          df_pivot.columns.str.replace(r'[A-Z]+(\d+).*', r'\1').astype(int)))
    pivot_cols.sort(key=itemgetter(1))
    return df_pivot[[x for x, y in pivot_cols]]
