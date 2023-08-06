# -*- coding: utf-8 -*-
"""
Functions for subtyping of reads (e.g. FASTQ) and contigs (e.g. FASTA) using bio_hansel-compatible subtyping schemes.
"""
import logging
import re
from typing import Optional, List, Dict, Union, Tuple, Set

import pandas as pd

from .aho_corasick import init_automaton, find_in_fasta, find_in_fastqs
from .const import COLUMNS_TO_REMOVE
from .qc import perform_quality_check, QC
from .subtype import Subtype
from .subtype_stats import SubtypeCounts
from .subtype_stats import subtype_counts
from .subtyping_params import SubtypingParams
from .utils import find_inconsistent_subtypes, get_scheme_fasta, get_scheme_version, init_subtyping_params


def subtype_reads_samples(reads: List[Tuple[List[str], str]],
                          scheme: str,
                          scheme_name: Optional[str] = None,
                          subtyping_params: Optional[SubtypingParams] = None,
                          scheme_subtype_counts: Optional[Dict[str, SubtypeCounts]] = None,
                          n_threads: int = 1) -> List[Tuple[Subtype, pd.DataFrame]]:
    """Subtype input genomes using a scheme.

    Args:
        reads: input genomes; tuple of list of FASTQ file paths and genome name
        scheme: bio_hansel scheme FASTA path
        scheme_name: optional scheme name
        subtyping_params: scheme specific subtyping parameters
        scheme_subtype_counts: summary information about scheme
        n_threads: number of threads to use for subtyping analysis

    Returns:
        List of tuple of Subtype and detailed subtyping results for each sample
    """
    if n_threads == 1:
        logging.info('Serial single threaded run mode on %s input genomes', len(reads))
        outputs = [subtype_reads(reads=fastq_files,
                                 genome_name=genome_name,
                                 scheme=scheme,
                                 scheme_name=scheme_name,
                                 subtyping_params=subtyping_params,
                                 scheme_subtype_counts=scheme_subtype_counts)
                   for fastq_files, genome_name in reads]
    else:
        outputs = parallel_query_reads(reads=reads,
                                       scheme=scheme,
                                       scheme_name=scheme_name,
                                       subtyping_params=subtyping_params,
                                       scheme_subtype_counts=scheme_subtype_counts,
                                       n_threads=n_threads)
    return outputs


def subtype_contigs_samples(input_genomes: List[Tuple[str, str]],
                            scheme: str,
                            scheme_name: Optional[str] = None,
                            subtyping_params: Optional[SubtypingParams] = None,
                            scheme_subtype_counts: Optional[Dict[str, SubtypeCounts]] = None,
                            n_threads: int = 1) -> List[Tuple[Subtype, pd.DataFrame]]:
    """Subtype input genomes using a scheme.

    Args:
        input_genomes: input genomes; tuple of FASTA file path and genome name
        scheme: bio_hansel scheme FASTA path
        scheme_name: optional scheme name
        subtyping_params: scheme specific subtyping parameters
        scheme_subtype_counts: summary information about scheme
        n_threads: number of threads to use for subtyping analysis

    Returns:
        List of tuple of Subtype and detailed subtyping results for each sample
    """
    if n_threads == 1:
        logging.info('Serial single threaded run mode on %s input genomes', len(input_genomes))
        outputs = [subtype_contigs(fasta_path=input_fasta,
                                   genome_name=genome_name,
                                   scheme=scheme,
                                   scheme_name=scheme_name,
                                   subtyping_params=subtyping_params,
                                   scheme_subtype_counts=scheme_subtype_counts)
                   for input_fasta, genome_name in input_genomes]
    else:
        outputs = parallel_query_contigs(input_genomes, scheme, scheme_name, subtyping_params, scheme_subtype_counts,
                                         n_threads)
    return outputs


def subtype_contigs(fasta_path: str,
                    genome_name: str,
                    scheme: str,
                    subtyping_params: Optional[SubtypingParams] = None,
                    scheme_name: Optional[str] = None,
                    scheme_subtype_counts: Optional[Dict[str, SubtypeCounts]] = None) \
        -> Tuple[Subtype, pd.DataFrame]:
    """Subtype input contigs using a particular scheme.

    Args:
        fasta_path: Input FASTA file path
        genome_name: Input genome name
        scheme: bio_hansel scheme FASTA path
        subtyping_params: scheme specific subtyping parameters
        scheme_name: optional scheme name
        scheme_subtype_counts: summary information about scheme

    Returns:
        - Subtype result
        - pd.DataFrame of detailed subtyping results
    """
    scheme_fasta = get_scheme_fasta(scheme)
    if scheme_subtype_counts is None:
        scheme_subtype_counts = subtype_counts(scheme_fasta)
    if subtyping_params is None:
        subtyping_params = init_subtyping_params(scheme=scheme)
    scheme_version = get_scheme_version(scheme)
    st = Subtype(sample=genome_name,
                 file_path=fasta_path,
                 scheme=scheme_name or scheme,
                 scheme_version=scheme_version,
                 scheme_subtype_counts=scheme_subtype_counts)

    automaton = init_automaton(scheme_fasta)
    df = find_in_fasta(automaton, fasta_path)

    if df is None or df.shape[0] == 0:
        logging.warning('No subtyping kmer matches for input "%s" for scheme "%s"', fasta_path, scheme)
        st.qc_status = QC.FAIL
        st.qc_message = QC.NO_TARGETS_FOUND
        st.are_subtypes_consistent = False
        return st, empty_results(st)

    refpositions = [x for x, y in df.kmername.str.split('-')]
    subtypes = [y for x, y in df.kmername.str.split('-')]
    df['refposition'] = [int(x.replace('negative', '')) for x in refpositions]
    df['subtype'] = subtypes
    df['is_pos_kmer'] = ~df.kmername.str.contains('negative')
    process_subtyping_results(st, df, scheme_subtype_counts)
    st.qc_status, st.qc_message = perform_quality_check(st, df, subtyping_params)

    logging.info(st)

    df['sample'] = genome_name
    df['file_path'] = fasta_path
    df['scheme'] = scheme_name or scheme
    df['scheme_version'] = scheme_version
    df['qc_status'] = st.qc_status
    df['qc_message'] = st.qc_message

    df = df[df.columns[~df.columns.isin(COLUMNS_TO_REMOVE)]]
    return st, df


def parallel_query_contigs(input_genomes: List[Tuple[str, str]],
                           scheme: str,
                           scheme_name: Optional[str] = None,
                           subtyping_params: Optional[SubtypingParams] = None,
                           scheme_subtype_counts: Optional[Dict[str, SubtypeCounts]] = None,
                           n_threads: int = 1):
    """Parallel subtyping of input contigs

    Subtype and analyse each input in parallel using a multiprocessing thread pool.

    Args:
        input_genomes: Input genome FASTA paths
        scheme: bio_hansel scheme FASTA path to subtype with
        scheme_name: optional scheme name
        subtyping_params: scheme specific subtyping parameters
        scheme_subtype_counts: scheme summary information
        n_threads: Number of threads to use

    Returns:
        A list of tuples of Subtype results and a pd.DataFrame of detailed subtyping results for each input
    """
    from multiprocessing import Pool
    logging.info('Initializing thread pool with %s threads', n_threads)
    pool = Pool(processes=n_threads)
    logging.info('Running analysis asynchronously on %s input genomes', len(input_genomes))
    res = [pool.apply_async(subtype_contigs, (input_fasta,
                                              genome_name,
                                              scheme,
                                              subtyping_params,
                                              scheme_name,
                                              scheme_subtype_counts))
           for input_fasta, genome_name in input_genomes]
    logging.info('Parallel analysis complete! Retrieving analysis results')
    return [x.get() for x in res]


def parallel_query_reads(reads: List[Tuple[List[str], str]],
                         scheme: str,
                         scheme_name: Optional[str] = None,
                         subtyping_params: Optional[SubtypingParams] = None,
                         scheme_subtype_counts: Optional[Dict[str, SubtypeCounts]] = None,
                         n_threads: int = 1) -> List[Tuple[Subtype, pd.DataFrame]]:
    """Parallel subtyping of input reads

    Subtype and analyse each input in parallel using a multiprocessing thread pool.

    Args:
        reads: Input reads; list of tuples of FASTQ file paths and genome names
        scheme: bio_hansel scheme FASTA path
        scheme_name: optional scheme name
        subtyping_params: scheme specific subtyping parameters
        scheme_subtype_counts: scheme summary information
        n_threads: number of threads to use

    Returns:
        A list of tuples of Subtype results and a pd.DataFrame of detailed subtyping results for each input
    """
    from multiprocessing import Pool
    logging.info('Initializing thread pool with %s threads', n_threads)
    pool = Pool(processes=n_threads)
    logging.info('Running analysis asynchronously on %s input genomes', len(reads))
    res = [pool.apply_async(subtype_reads, (fastqs,
                                            genome_name,
                                            scheme,
                                            scheme_name,
                                            subtyping_params,
                                            scheme_subtype_counts))
           for fastqs, genome_name in reads]
    logging.info('Parallel analysis complete! Retrieving analysis results')
    return [x.get() for x in res]


def get_kmer_fraction(row):
    """Calculate the percentage frequency of a given position

    Args:
        row: BioHansel k-mer frequence pandas df row
    Returns:
        - float of percentage abundance
    """
    total_freq = row.total_refposition_kmer_frequency
    return row.freq / total_freq if total_freq > 0 else 0.0


def calc_kmer_fraction(df):
    """Calculate the percentage each k-mer frequency represents for a given position

    Args:
        df: BioHansel k-mer frequence pandas df

    Returns:
        - pd.DataFrame with k-mers with kmer_fraction and total_refposition_kmer_frequency columns added
    """
    position_frequencies = df[['refposition', 'freq']].groupby(['refposition']).sum().to_dict()
    df['total_refposition_kmer_frequency'] = df.apply(lambda row: position_frequencies['freq'].get(row.refposition, 0),
                                                      axis=1)
    df['kmer_fraction'] = df.apply(get_kmer_fraction, axis=1)

    return df


def subtype_reads(reads: Union[str, List[str]],
                  genome_name: str,
                  scheme: str,
                  scheme_name: Optional[str] = None,
                  subtyping_params: Optional[SubtypingParams] = None,
                  scheme_subtype_counts: Optional[Dict[str, SubtypeCounts]] = None) \
        -> Tuple[Subtype, Optional[pd.DataFrame]]:
    """Subtype input reads using a particular scheme.

    Args:
        reads: Input FASTQ file path(s)
        genome_name: Input genome name
        scheme: bio_hansel scheme FASTA path
        scheme_name: optional scheme name
        subtyping_params: scheme specific subtyping parameters
        scheme_subtype_counts: summary information about scheme

    Returns:
        - Subtype result
        - pd.DataFrame of detailed subtyping results
    """
    scheme_fasta = get_scheme_fasta(scheme)
    if scheme_subtype_counts is None:
        scheme_subtype_counts = subtype_counts(scheme_fasta)
    if subtyping_params is None:
        subtyping_params = init_subtyping_params(scheme=scheme)
    scheme_version = get_scheme_version(scheme)

    st = Subtype(sample=genome_name,
                 file_path=reads,
                 scheme=scheme_name or scheme,
                 scheme_version=scheme_version,
                 scheme_subtype_counts=scheme_subtype_counts)

    automaton = init_automaton(scheme_fasta)
    if isinstance(reads, str):
        df = find_in_fastqs(automaton, reads)
    elif isinstance(reads, list):
        df = find_in_fastqs(automaton, *reads)
    else:
        raise ValueError('Unexpected type "{}" for "reads": {}'.format(type(reads), reads))

    if df is None or df.shape[0] == 0:
        logging.warning('No subtyping kmer matches for input "%s" for scheme "%s"', reads, scheme)
        st.are_subtypes_consistent = False
        st.qc_status = QC.FAIL
        st.qc_message = QC.NO_TARGETS_FOUND
        return st, empty_results(st)

    refpositions = [x for x, y in df.kmername.str.split('-')]
    subtypes = [y for x, y in df.kmername.str.split('-')]
    df['refposition'] = [int(x.replace('negative', '')) for x in refpositions]
    df['subtype'] = subtypes
    df['is_pos_kmer'] = ~df.kmername.str.contains('negative')
    df['is_kmer_freq_okay'] = (df.freq >= subtyping_params.min_kmer_freq) & (df.freq <= subtyping_params.max_kmer_freq)
    # apply a scaled approach for filtering of k-mers required for high coverage amplicon data
    df = calc_kmer_fraction(df)
    df['is_kmer_fraction_okay'] = df.kmer_fraction >= subtyping_params.min_kmer_frac
    st.avg_kmer_coverage = df['freq'].mean()
    st, filtered_df = process_subtyping_results(st, df[(df.is_kmer_freq_okay & df.is_kmer_fraction_okay)],
                                                scheme_subtype_counts)
    st.qc_status, st.qc_message = perform_quality_check(st, filtered_df, subtyping_params)
    df['file_path'] = str(st.file_path)
    df['sample'] = genome_name
    df['scheme'] = scheme_name or scheme
    df['scheme_version'] = scheme_version
    df['qc_status'] = st.qc_status
    df['qc_message'] = st.qc_message
    df = df[df.columns[~df.columns.isin(COLUMNS_TO_REMOVE)]]
    return st, df


def process_subtyping_results(st: Subtype,
                              df: pd.DataFrame,
                              scheme_subtype_counts: Dict[str, SubtypeCounts]) -> Tuple[Subtype, pd.DataFrame]:
    """Process the subtyping results to get the final subtype result and summary stats

    Args:
        st: Subtype result
        df: Subtyping results
        scheme_subtype_counts: Subtyping scheme summary info
    Returns:
        Tuple of `st` and `df`
    """
    dfpos = df[df.is_pos_kmer]
    dfpos_highest_res = highest_resolution_subtype_results(dfpos)
    subtype_list = [x for x in dfpos_highest_res.subtype.unique()]
    st = set_subtype_results(st, dfpos, subtype_list)
    st = set_inconsistent_subtypes(st, find_inconsistent_subtypes(sorted_subtype_ints(dfpos.subtype)))
    st = set_subtyping_stats(st, df, dfpos, dfpos_highest_res, subtype_list, scheme_subtype_counts)
    st.non_present_subtypes = absent_downstream_subtypes(st.subtype, df.subtype, list(scheme_subtype_counts.keys()))
    st.missing_nested_subtypes = missing_nested_subtypes(st.subtype, set(dfpos.subtype.unique()))
    return st, df


def set_subtype_results(st: Subtype, df_positive: pd.DataFrame, subtype_list: List[str]) -> Subtype:
    """Set subtype results

    Args:
        st: Subtype result
        df_positive: Positive kmers subtyping results
        subtype_list: List of subtypes found
    """
    st.subtype = '; '.join(subtype_list)
    st.kmers_matching_subtype = '; '.join(subtype_list)
    pos_subtypes_str = [x for x in df_positive.subtype.unique()]
    pos_subtypes_str.sort(key=lambda x: len(x))
    st.all_subtypes = '; '.join(pos_subtypes_str)
    return st


def set_subtyping_stats(st: Subtype,
                        df: pd.DataFrame,
                        dfpos: pd.DataFrame,
                        dfpos_highest_res: pd.DataFrame,
                        subtype_list: List[str],
                        scheme_subtype_counts: Dict[str, SubtypeCounts]) -> Subtype:
    """Set subtyping result stats

    - `n_kmers_matching_subtype`: # kmers matching final subtype
    - `n_kmers_matching_all`: # kmers found
    - `n_kmers_matching_positive`: # positive kmers found
    - `n_kmers_matching_negative`:  # negative kmers found
    - `n_kmers_matching_all_expected`: expected # of all kmers found for each subtype
    - `n_kmers_matching_positive_expected`: expected # of positive kmers found for each subtype
    - `n_kmers_matching_subtype_expected`: expected # of subtype-specific kmers found for each subtype

    Args:
        st: Subtype result
        df: Subtyping results
        dfpos: Positive kmer subtyping results
        dfpos_highest_res: Final subtype specific subtyping results
        subtype_list: List of subtypes found
        scheme_subtype_counts: Subtyping scheme summary info
    """
    st.n_kmers_matching_subtype = dfpos_highest_res.shape[0]
    st.n_kmers_matching_all = df.kmername.unique().size
    st.n_kmers_matching_positive = dfpos.kmername.unique().size
    st.n_kmers_matching_negative = df[~df.is_pos_kmer].shape[0]
    st.n_kmers_matching_all_expected = ';'.join([str(scheme_subtype_counts[x].all_kmer_count) for x in subtype_list])
    st.n_kmers_matching_positive_expected = ';'.join(
        [str(scheme_subtype_counts[x].positive_kmer_count) for x in subtype_list])
    st.n_kmers_matching_subtype_expected = ';'.join(
        [str(scheme_subtype_counts[x].subtype_kmer_count) for x in subtype_list])
    return st


def highest_resolution_subtype_results(df: pd.DataFrame) -> pd.DataFrame:
    """Get the highest resolution subtype results

    Where the highest resolution result has the most periods ('.') in its designation.

    Args:
        df: positive subtyping results

    Returns:
        Highest resolution (most periods in subtype) subtyping results
    """
    subtype_series: pd.Series = df.subtype
    subtype_lens = subtype_series.str.count(r'\.')
    max_subtype_strlen = subtype_lens.max()
    return df[subtype_lens == max_subtype_strlen]


def sorted_subtype_ints(subtypes: pd.Series) -> List[List[int]]:
    """Get the list of subtypes as lists of integers sorted by subtype resolution

    Where the subtype resolution is determined by the number of periods ('.') in the subtype.

    Args:
        subtypes: pd.Series of subtype strings

    Return:
        list of subtypes as lists of integers sorted by subtype resolution
    """
    subtypes_ints = [[int(y) for y in x.split('.')] for x in subtypes.unique()]
    subtypes_ints.sort(key=lambda a: len(a))
    return subtypes_ints


def absent_downstream_subtypes(subtype: str,
                               subtypes: pd.Series,
                               scheme_subtypes: List[str]) -> Optional[List[str]]:
    """Find the downstream subtypes that are not present in the results

    Args:
        subtype: Final subtype result
        subtypes: Subtypes found
        scheme_subtypes: Possible subtyping scheme subtypes

    Returns:
         List of downstream subtypes that are not present in the results or `None` if all immediately downstream
         subtypes are present.
    """
    escaped_subtype = re.escape(subtype)
    re_subtype = re.compile(r'^{}\.\d+$'.format(escaped_subtype))
    downstream_subtypes = [s for s in scheme_subtypes if re_subtype.search(s)]
    absentees = [x for x in downstream_subtypes if not (subtypes == x).any()]
    return absentees if absentees else None


def get_missing_internal_subtypes(st_vals: List[str],
                                  pos_subtypes_set: Set[str]) -> Set[str]:
    """Compare nested subtypes from the final subtype call to positive subtypes found

    Args:
        st_vals: Hierarchical subtype values
        pos_subtypes_set: Set of positive subtypes

    Returns:
        Set of missing nested hierarchical subtypes
    """
    out = set()
    for i in range(len(st_vals)):
        sub_subtype = '.'.join(st_vals[0: i + 1])
        if sub_subtype not in pos_subtypes_set:
            out.add(sub_subtype)
    return out


def missing_nested_subtypes(subtype_result: str, positive_subtypes: Set[str]) -> Optional[str]:
    """Find nested subtypes that are missing from the final subtype call

    Args:
        subtype_result: Final subtype result
        positive_subtypes: Set of unique positive subtypes found

    Returns:
        String of missing hierarchical subtypes or `None` if there are no missing nested hierarchical subtypes.
    """
    subtypes = subtype_result.split(';')
    missing_subtypes_set = set()
    for subtype in subtypes:
        st_vals = subtype.split('.')
        missing_subtypes_set |= get_missing_internal_subtypes(st_vals, positive_subtypes)
    return '; '.join(missing_subtypes_set)


def set_inconsistent_subtypes(st: Subtype, inconsistent_subtypes: List[str]) -> Subtype:
    """Save the list of inconsistent subtypes, if any, to the Subtype result

    Args:
        st: Subtype result
        inconsistent_subtypes: List of inconsistent subtypes

    Returns:

    """
    if inconsistent_subtypes:
        st.are_subtypes_consistent = False
        st.inconsistent_subtypes = inconsistent_subtypes
    else:
        st.are_subtypes_consistent = True
        st.inconsistent_subtypes = None
    return st


def empty_results(st: Subtype) -> pd.DataFrame:
    """Get a results DataFrame with 1 entry when no results are retrieved.

    When the output DataFrame for subtyping is empty, generate a "dummy" DataFrame with one row showing that subtyping
    was performed on the sample, but no results were generated because nothing was found.

    Args:
        st: Subtype results; should be a null result

    Returns:
        pd.DataFrame with 1 row with null result
    """
    return pd.DataFrame({0: dict(sample=st.sample,
                                 file_path=st.file_path,
                                 subtype=st.subtype,
                                 refposition=None,
                                 is_pos_kmer=None,
                                 scheme=st.scheme,
                                 scheme_version=st.scheme_version,
                                 qc_status=st.qc_status,
                                 qc_message=st.qc_message)}).transpose()
