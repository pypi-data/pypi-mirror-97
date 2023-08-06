|logo|

|conda| |nbsp| |pypi| |nbsp|  |rtd| |nbsp| |license|


======  ===========
Master  |ci-master|
Dev     |ci-dev|
======  ===========

.. |logo| image:: logo.png
    :target: https://github.com/phac-nml/biohansel
.. |pypi| image:: https://badge.fury.io/py/bio-hansel.svg
    :target: https://pypi.python.org/pypi/bio_hansel/
.. |license| image:: https://img.shields.io/badge/License-Apache%20v2.0-blue.svg
    :target: http://www.apache.org/licenses/LICENSE-2.0
.. |ci-master| image:: https://github.com/phac-nml/biohansel/workflows/CI/badge.svg?branch=master
    :target: https://github.com/phac-nml/biohansel/actions
.. |ci-dev| image:: https://github.com/phac-nml/biohansel/workflows/CI/badge.svg?branch=development
    :target: https://github.com/phac-nml/biohansel/actions
.. |conda|   image:: https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg
    :target: https://bioconda.github.io/recipes/bio_hansel/README.html
.. |nbsp| unicode:: 0xA0
    :trim:
.. |rtd| image:: https://readthedocs.org/projects/pip/badge/?version=latest&style=flat
    :target: https://bio-hansel.readthedocs.io/en/readthedocs/

Subtype microbial whole-genome sequencing (WGS) data using SNV targeting k-mer subtyping schemes.

Includes 33 bp k-mer SNV subtyping schemes for *Salmonella enterica* subsp. enterica serovars Heidelberg, Enteritidis, and Typhimurium genomes developed by Genevieve Labbe et al., and for *S*. ser Typhi adapted from `Wong et al. <https://www.nature.com/articles/ncomms12827)>`_, `Britto et al. <https://journals.plos.org/plosntds/article?id=10.1371/journal.pntd.0006408>`_, `Rahman et al. <https://journals.plos.org/plosntds/article?id=10.1371/journal.pntd.0008036>`_, and `Klemm et al. <https://mbio.asm.org/content/9/1/e00105-18>`_.

Works on genome assemblies (FASTA files) or reads (FASTQ files)! Accepts Gzipped FASTA/FASTQ files as input!

Also includes a *Mycobacterium tuberculosis* lineage scheme adapted from `Coll et al. <https://www.nature.com/articles/ncomms5812>`_ by Daniel Kein.


Citation
========

If you find the ``biohansel`` tool useful, please cite as:

.. epigraph::

    Rapid and accurate SNP genotyping of clonal bacterial pathogens with BioHansel.
    Geneviève Labbé, Peter Kruczkiewicz, Philip Mabon, James Robertson, Justin Schonfeld, Daniel Kein, Marisa A. Rankin, Matthew Gopez, Darian Hole, David Son, Natalie Knox, Chad R. Laing, Kyrylo Bessonov, Eduardo Taboada, Catherine Yoshida, Kim Ziebell, Anil Nichani, Roger P. Johnson, Gary Van Domselaar and John H.E. Nash.
    bioRxiv 2020.01.10.902056; doi: https://doi.org/10.1101/2020.01.10.902056


Read_The_Docs
==============

More in-depth information on running and installing biohansel can be found on the `biohansel readthedocs page <https://bio-hansel.readthedocs.io/en/readthedocs/>`_.


Requirements and Dependencies
=============================

Each new build of ``biohansel`` is automatically tested on Linux using `Continuous Integration <https://travis-ci.org/phac-nml/bio_hansel/branches>`_. ``biohansel`` has been confirmed to work on Mac OSX (versions 10.13.5 Beta and 10.12.6) when installed with Conda_.

These are the dependencies required for ``biohansel``:

- Python_ (>=v3.6)
    - numpy_ >=1.12.1
    - pandas_ >=0.20.1
    - pyahocorasick_ >=1.1.6
    - attrs_


Installation
============

With Conda_
-----------

Install ``biohansel`` from Bioconda_ with Conda_ (`Conda installation instructions <https://bioconda.github.io/#install-conda>`_):

.. code-block:: bash

    # setup Conda channels for Bioconda and Conda-Forge (https://bioconda.github.io/#set-up-channels)
    conda config --add channels defaults
    conda config --add channels conda-forge
    conda config --add channels bioconda
    # install biohansel
    conda install bio_hansel

With pip_ from PyPI_
---------------------

Install ``biohansel`` from PyPI_ with pip_:

.. code-block:: bash

    pip install bio_hansel

With pip_ from Github
---------------------

Or install the latest master branch version directly from Github:

.. code-block:: bash

    pip install git+https://github.com/phac-nml/biohansel.git@master

Install into Galaxy_ (version >= 17.01)
---------------------------------------

Install ``biohansel`` from the main Galaxy_ toolshed:

https://toolshed.g2.bx.psu.edu/view/nml/biohansel/ba6a0af656a6


Usage
=====

If you run ``hansel -h``, you should see the following usage statement:

.. code-block::

    usage: hansel [-h] [-s SCHEME] [--scheme-name SCHEME_NAME]
                  [-M SCHEME_METADATA] [-p forward_reads reverse_reads]
                  [-i fasta_path genome_name] [-D INPUT_DIRECTORY]
                  [-o OUTPUT_SUMMARY] [-O OUTPUT_KMER_RESULTS]
                  [-S OUTPUT_SIMPLE_SUMMARY] [--force] [--json]
                  [--min-kmer-freq MIN_KMER_FREQ] [--min-kmer-frac MIN_KMER_FRAC]
                  [--max-kmer-freq MAX_KMER_FREQ]
                  [--low-cov-depth-freq LOW_COV_DEPTH_FREQ]
                  [--max-missing-kmers MAX_MISSING_KMERS]
                  [--min-ambiguous-kmers MIN_AMBIGUOUS_KMERS]
                  [--low-cov-warning LOW_COV_WARNING]
                  [--max-intermediate-kmers MAX_INTERMEDIATE_KMERS]
                  [--max-degenerate-kmers MAX_DEGENERATE_KMERS] [-t THREADS] [-v]
                  [-V]
                  [F [F ...]]

    BioHansel version 2.5.1: Subtype microbial genomes using SNV targeting k-mer subtyping schemes.

    Built-in schemes:

    * heidelberg:  Salmonella enterica spp. enterica serovar Heidelberg
    * enteritidis: Salmonella enterica spp. enterica serovar Enteritidis
    * typhimurium: Salmonella enterica spp. enterica serovar Typhimurium
    * typhi:       Salmonella enterica spp. enterica serovar Typhi
    * tb_lineage:  Mycobacterium tuberculosis

    Developed by Geneviève Labbé, Peter Kruczkiewicz, Philip Mabon, James Robertson, Justin Schonfeld, Daniel Kein, Marisa A. Rankin, Matthew Gopez, Darian Hole, David Son, Natalie Knox, Chad R. Laing, Kyrylo Bessonov, Eduardo Taboada, Catherine Yoshida, Kim Ziebell, Anil Nichani, Roger P. Johnson, Gary Van Domselaar and John H.E. Nash.

    positional arguments:
      F                     Input genome FASTA/FASTQ files (can be Gzipped)

    optional arguments:
      -h, --help            show this help message and exit
      -s SCHEME, --scheme SCHEME
                            Scheme to use for subtyping (built-in: "heidelberg",
                            "enteritidis", "typhi", "typhimurium", "tb_lineage";
                            OR user-specified: /path/to/user/scheme)
      --scheme-name SCHEME_NAME
                            Custom user-specified SNP substyping scheme name
      -M SCHEME_METADATA, --scheme-metadata SCHEME_METADATA
                            Scheme subtype metadata table (tab-delimited file with
                            ".tsv" or ".tab" extension or CSV with ".csv"
                            extension format accepted; MUST contain column called
                            "subtype")
      -p forward_reads reverse_reads, --paired-reads forward_reads reverse_reads
                            FASTQ paired-end reads
      -i fasta_path genome_name, --input-fasta-genome-name fasta_path genome_name
                            input fasta file path AND genome name
      -D INPUT_DIRECTORY, --input-directory INPUT_DIRECTORY
                            directory of input fasta files (.fasta|.fa|.fna) or
                            FASTQ files (paired FASTQ should have same basename
                            with "_\d\.(fastq|fq)" postfix to be automatically
                            paired) (files can be Gzipped)
      -o OUTPUT_SUMMARY, --output-summary OUTPUT_SUMMARY
                            Subtyping summary output path (tab-delimited)
      -O OUTPUT_KMER_RESULTS, --output-kmer-results OUTPUT_KMER_RESULTS
                            Subtyping kmer matching output path (tab-delimited)
      -S OUTPUT_SIMPLE_SUMMARY, --output-simple-summary OUTPUT_SIMPLE_SUMMARY
                            Subtyping simple summary output path
      --force               Force existing output files to be overwritten
      --json                Output JSON representation of output files
      --min-kmer-freq MIN_KMER_FREQ
                            Min k-mer freq/coverage
      --min-kmer-frac MIN_KMER_FRAC
                            Proportion of k-mer required for detection (0.0 - 1)
      --max-kmer-freq MAX_KMER_FREQ
                            Max k-mer freq/coverage
      --low-cov-depth-freq LOW_COV_DEPTH_FREQ
                            Frequencies below this coverage are considered low
                            coverage
      --max-missing-kmers MAX_MISSING_KMERS
                            Decimal proportion of maximum allowable missing kmers
                            before being considered an error. (0.0 - 1.0)
      --min-ambiguous-kmers MIN_AMBIGUOUS_KMERS
                            Minimum number of missing kmers to be considered an
                            ambiguous result
      --low-cov-warning LOW_COV_WARNING
                            Overall kmer coverage below this value will trigger a
                            low coverage warning
      --max-intermediate-kmers MAX_INTERMEDIATE_KMERS
                            Decimal proportion of maximum allowable missing kmers
                            to be considered an intermediate subtype. (0.0 - 1.0)
      --max-degenerate-kmers MAX_DEGENERATE_KMERS
                            Maximum number of scheme k-mers allowed before
                            quitting with a usage warning. Default is 100000
      -t THREADS, --threads THREADS
                            Number of parallel threads to run analysis (default=1)
      -v, --verbose         Logging verbosity level (-v == show warnings; -vvv ==
                            show debug info)
      -V, --version         show program's version number and exit



Example Usage
=============

Analysis of a single FASTA file
-------------------------------

.. code-block:: bash

    hansel -s heidelberg -vv -o results.tab -O match_results.tab /path/to/SRR1002850.fasta


Contents of ``results.tab``:

.. code-block::

    sample  scheme  subtype all_subtypes    kmers_matching_subtype  are_subtypes_consistent inconsistent_subtypes   n_kmers_matching_all    n_kmers_matching_all_total  n_kmers_matching_positive   n_kmers_matching_positive_total n_kmers_matching_subtype    n_kmers_matching_subtype_total  file_path
    SRR1002850  heidelberg  2.2.2.2.1.4 2; 2.2; 2.2.2; 2.2.2.2; 2.2.2.2.1; 2.2.2.2.1.4  1037658-2.2.2.2.1.4; 2154958-2.2.2.2.1.4; 3785187-2.2.2.2.1.4   True        202 202 17  17  3   3   SRR1002850.fasta


Contents of ``match_results.tab``:

.. code-block::

    kmername    stitle  pident  length  mismatch    gapopen qstart  qend    sstart  send    evalue  bitscore    qlen    slen    seq coverage    is_trunc    refposition subtype is_pos_kmer sample  file_path   scheme
    775920-2.2.2.2  NODE_2_length_512016_cov_46.4737_ID_3   100.0   33  0   0   1   33  474875  474907  2.0000000000000002e-11  62.1    33  512016  GTTCAGGTGCTACCGAGGATCGTTTTTGGTGCG   1.0 False   775920  2.2.2.2 True    SRR1002850  SRR1002850.fasta   heidelberg
    negative3305400-2.1.1.1 NODE_3_length_427905_cov_48.1477_ID_5   100.0   33  0   0   1   33  276235  276267  2.0000000000000002e-11  62.1    33  427905  CATCGTGAAGCAGAACAGACGCGCATTCTTGCT   1.0 False   negative3305400 2.1.1.1 False   SRR1002850  SRR1002850.fasta   heidelberg
    negative3200083-2.1 NODE_3_length_427905_cov_48.1477_ID_5   100.0   33  0   0   1   33  170918  170950  2.0000000000000002e-11  62.1    33  427905  ACCCGGTCTACCGCAAAATGGAAAGCGATATGC   1.0 False   negative3200083 2.1 False   SRR1002850  SRR1002850.fasta   heidelberg
    negative3204925-2.2.3.1.5   NODE_3_length_427905_cov_48.1477_ID_5   100.0   33  0   0   1   33  175760  175792  2.0000000000000002e-11  62.1    33  427905  CTCGCTGGCAAGCAGTGCGGGTACTATCGGCGG   1.0 False   negative3204925 2.2.3.1.5   False   SRR1002850  SRR1002850.fasta   heidelberg
    negative3230678-2.2.2.1.1.1 NODE_3_length_427905_cov_48.1477_ID_5   100.0   33  0   0   1   33  201513  201545  2.0000000000000002e-11  62.1    33  427905  AGCGGTGCGCCAAACCACCCGGAATGATGAGTG   1.0 False   negative3230678 2.2.2.1.1.1 False   SRR1002850  SRR1002850.fasta   heidelberg
    negative3233869-2.1.1.1.1   NODE_3_length_427905_cov_48.1477_ID_5   100.0   33  0   0   1   33  204704  204736  2.0000000000000002e-11  62.1    33  427905  CAGCGCTGGTATGTGGCTGCACCATCGTCATTA   1.0 False   
    [Next 196 lines omitted.]


Analysis of a single FASTQ readset
----------------------------------

.. code-block:: bash

    hansel -s heidelberg -vv -t 4 -o results.tab -O match_results.tab -p SRR5646583_forward.fastqsanger SRR5646583_reverse.fastqsanger


Contents of ``results.tab``:

.. code-block::

    sample  scheme  subtype all_subtypes    kmers_matching_subtype  are_subtypes_consistent inconsistent_subtypes   n_kmers_matching_all    n_kmers_matching_all_total  n_kmers_matching_positive   n_kmers_matching_positive_total n_kmers_matching_subtype    n_kmers_matching_subtype_total  file_path
    SRR5646583  heidelberg  2.2.1.1.1.1 2; 2.2; 2.2.1; 2.2.1.1; 2.2.1.1.1; 2.2.1.1.1.1  1983064-2.2.1.1.1.1; 4211912-2.2.1.1.1.1    True        202 202 20  20  2   2   SRR5646583_forward.fastqsanger; SRR5646583_reverse.fastqsanger


Contents of ``match_results.tab``:

.. code-block::

    seq freq    sample  file_path   kmername    is_pos_kmer subtype refposition is_kmer_freq_okay   scheme
    ACGGTAAAAGAGGACTTGACTGGCGCGATTTGC   68  SRR5646583 SRR5646583_forward.fastqsanger; SRR5646583_reverse.fastqsanger    21097-2.2.1.1.1 True    2.2.1.1.1   21097   True    heidelberg
    AACCGGCGGTATTGGCTGCGGTAAAAGTACCGT   77  SRR5646583 SRR5646583_forward.fastqsanger; SRR5646583_reverse.fastqsanger    157792-2.2.1.1.1    True    2.2.1.1.1   157792  True    heidelberg
    CCGCTGCTTTCTGAAATCGCGCGTCGTTTCAAC   67  SRR5646583 SRR5646583_forward.fastqsanger; SRR5646583_reverse.fastqsanger    293728-2.2.1.1  True    2.2.1.1 293728  True    heidelberg
    GAATAACAGCAAAGTGATCATGATGCCGCTGGA   91  SRR5646583 SRR5646583_forward.fastqsanger; SRR5646583_reverse.fastqsanger    607438-2.2.1    True    2.2.1   607438  True    heidelberg
    CAGTTTTACATCCTGCGAAATGCGCAGCGTCAA   87  SRR5646583 SRR5646583_forward.fastqsanger; SRR5646583_reverse.fastqsanger    691203-2.2.1.1  True    2.2.1.1 691203  True    heidelberg
    CAGGAGAAAGGATGCCAGGGTCAACACGTAAAC   33  SRR5646583 SRR5646583_forward.fastqsanger; SRR5646583_reverse.fastqsanger    944885-2.2.1.1.1    True    2.2.1.1.1   944885  True    heidelberg
    [Next 200 lines omitted.]

Analysis of all FASTA/FASTQ files in a directory
------------------------------------------------

.. code-block:: bash

    hansel -s heidelberg -vv --threads <n_cpu> -o results.tab -O match_results.tab -D /path/to/fastas_or_fastqs/


``biohansel`` will only attempt to analyze the FASTA/FASTQ files within the specified directory and will not descend into any subdirectories!

Metadata addition to analysis
-----------------------------

Add subtype metadata to your analysis results with `-M your-subtype-metadata.tsv`:

.. code-block:: bash

    hansel -s heidelberg \
      -M your-subtype-metadata.tsv \
      -o results.tab \
      -O match_results.tab \
      -D ~/your-reads-directory/

Your metadata table **must** contain a field with the field name `subtype`, e.g.

.. list-table::
   :header-rows: 1

   * - subtype
     - host_association
     - geoloc
     - genotype_alternative
   * - 1
     - human
     - Canada
     - A
   * - 2
     - cow
     - USA
     - B

``biohansel`` accepts metadata table files with the following formats and extensions:

.. list-table:: 
   :header-rows: 1

   * - Format
     - Extension
     - Example Filename
   * - Tab-delimited table/tab-separated values (TSV)
     - `.tsv`
     - `my-metadata-table.tsv`
   * - Tab-delimited table/tab-separated values (TSV)
     - `.tab`
     - `my-metadata-table.tab`
   * - Comma-separated values (CSV)
     - `.csv`
     - `my-metadata-table.csv`


Development
===========


Get the latest development code using Git from GitHub:

.. code-block:: bash

    git clone https://github.com/phac-nml/biohansel.git
    cd biohansel/
    git checkout development
    # Create a virtual environment (virtualenv) for development
    virtualenv -p python3 .venv
    # Activate the newly created virtualenv
    source .venv/bin/activate
    # Install biohansel into the virtualenv in "editable" mode
    pip install -e .


Run tests with pytest_:

.. code-block:: bash

    # In the biohansel/ root directory, install pytest for running tests
    pip install pytest
    # Run all tests in tests/ directory
    pytest
    # Or run a specific test module
    pytest -s tests/test_qc.py



Legal
=====

Copyright Government of Canada 2017

Written by: National Microbiology Laboratory, Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

Contact
=======

**Gary van Domselaar**: gary.vandomselaar@canada.ca


.. _PyPI: https://pypi.org/project/bio-hansel/
.. _Conda: https://conda.io/docs/
.. _Bioconda: https://bioconda.github.io/
.. _pip: https://pip.pypa.io/en/stable/quickstart/
.. _numpy: http://www.numpy.org/
.. _pandas: http://pandas.pydata.org/
.. _pyahocorasick: http://pyahocorasick.readthedocs.io/en/latest/
.. _attrs: http://www.attrs.org/en/stable/
.. _Python: https://www.python.org/
.. _Galaxy: https://galaxyproject.org/
.. _pytest: https://docs.pytest.org/en/latest/
