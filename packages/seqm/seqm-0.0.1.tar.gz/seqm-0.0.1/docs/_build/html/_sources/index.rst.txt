======================================
``seqm`` - genomic sequence metrics
======================================


Overview
========

This package provides python utilities for sequence comparison, quantification, and feature extraction.

The `seqm <https://github.com/atgtag/seqm>`_ module contains functions for calculating sequence-related distance and complexity metrics, commonly used in language processing and next-generation sequencing:

.. code-block:: python

    >>> import seqm
    >>> seqm.hamming('ATTATT', 'ATTAGT')
    1
    >>> seqm.edit('ATTATT', 'ATAGT')
    2
    >>> seqm.polydict('AAAACCGT')
    {'A': 4, 'C': 2, 'G': 1, 'T': 1}
    >>> seqm.polylength('AAAACCGT')
    4
    >>> seqm.entropy('AGGATAAG')
    1.40
    >>> seqm.gc_percent('AGGATAAG')
    0.375
    >>> seqm.gc_skew('AGGATAAG')
    3.0
    >>> seqm.gc_shift('AGGATAAG')
    1.67
    >>> seqm.dna_weight('AGGATAAG')
    3968.59
    >>> seqm.rna_weight('AGGATAAG')
    4082.59
    >>> seqm.aa_weight('AGGATAAG')
    700.8
    >>> seqm.zipsize('AGGATAAGAGATAGATTT')
    22


For more information on available functionality, see the `Usage <./usage.html>`_ section of the documentation.


Content
=======

.. toctree::
   :maxdepth: 3

   installation
   usage
   api


Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
