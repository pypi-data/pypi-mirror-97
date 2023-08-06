====
seqm
====

Python utilities for sequence comparison, quantification, and feature extraction.


Installation
============

.. code-block:: bash

    ~$ pip install seqm


Documentation
=============

Documentation for the package can be found `here <http://github.com/genova-io/seqm/latest/index.html>`_.


Usage
-----

The `seqm <http://github.com/genova-io/seqm/latest/index.html>`_ module contains functions for calculating sequence-related distance and complexity metrics, commonly used in language processing and next-generation sequencing. It has a simple and consistent API that be used for investigating sequence characteristics:

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
    >>> seqm.tm('AGGATAAGAGATAGATTT')
    39.31
    >>> seqm.zipsize('AGGATAAGAGATAGATTT')
    22


It also has a ``Sequence`` object for object-based access to these properties:

.. code-block:: python

    >>> import seqm
    >>> seq = seqm.Sequence('AAAACCGT')
    >>> seq.hamming('AAAAGCGT')
    1
    >>> seq.gc_percent
    0.375
    >>> seq.revcomplement
    ACGTACGT
    >>> seq.dna_weight
    3895.59
    >>> # ... and so on ...


All of the metrics available in the repository are listed below, and can also be found in the `API <http://github.com/genova-io/seqm/latest/api.html>`_ section of the documentation.


Sequence Quantification
+++++++++++++++++++++++

+---------------------------------+------------------------------------------------------------+
| Function                        | Metric                                                     |
+=================================+============================================================+
| ``seqm.polydict``               | Length of longest homopolymer for all bases in sequence.   |
+---------------------------------+------------------------------------------------------------+
| ``seqm.polylength``             | Length of longest homopolymer in sequence.                 |
+---------------------------------+------------------------------------------------------------+
| ``seqm.entropy``                | Shannon entropy for bases in sequence.                     |
+---------------------------------+------------------------------------------------------------+
| ``seqm.gc_percent``             | Percentage of GC bases in sequence relative to all bases.  |
+---------------------------------+------------------------------------------------------------+
| ``seqm.gc_skew``                | GC skew for sequence:  (#G - #C)/(#G + #C).                |
+---------------------------------+------------------------------------------------------------+
| ``seqm.gc_shift``               | GC shift for sequence: (#A + #T)/(#G + #C)                 |
+---------------------------------+------------------------------------------------------------+
| ``seqm.dna_weight``             | Molecular weight for sequence with DNA backbone.           |
+---------------------------------+------------------------------------------------------------+
| ``seqm.rna_weight``             | Molecular weight for sequence with RNA backbone.           |
+---------------------------------+------------------------------------------------------------+
| ``seqm.aa_weight``              | Molecular weight for amino acid sequence.                  |
+---------------------------------+------------------------------------------------------------+
| ``seqm.tm``                     | Melting temperature of sequence.                           |
+---------------------------------+------------------------------------------------------------+
| ``seqm.zipsize``                | Compressibility of sequence.                               |
+---------------------------------+------------------------------------------------------------+


Domain Conversion
+++++++++++++++++

+---------------------------------+------------------------------------------------------------+
| Function                        | Conversion                                                 |
+=================================+============================================================+
| ``seqm.revcomplement``          | Length of longest homopolymer for all bases in sequence.   |
+---------------------------------+------------------------------------------------------------+
| ``seqm.complement``             | Length of longest homopolymer in sequence.                 |
+---------------------------------+------------------------------------------------------------+
| ``seqm.aa``                     | Shannon entropy for bases in sequence.                     |
+---------------------------------+------------------------------------------------------------+
| ``seqm.wrap``                   | Percentage of GC bases in sequence relative to all bases.  |
+---------------------------------+------------------------------------------------------------+
| ``seqm.likelihood``             | GC skew for sequence:  (#G - #C)/(#G + #C).                |
+---------------------------------+------------------------------------------------------------+
| ``seqm.qscore``                 | GC shift for sequence: (#A + #T)/(#G + #C)                 |
+---------------------------------+------------------------------------------------------------+


Distance Metrics
++++++++++++++++

+---------------------------------+------------------------------------------------------------+
| Function                        | Distance Metric                                            |
+=================================+============================================================+
| ``seqm.hamming``                | Hamming distance between sequences.                        |
+---------------------------------+------------------------------------------------------------+
| ``seqm.edit``                   | Edit (levenshtein) distance between sequences              |
+---------------------------------+------------------------------------------------------------+


Utilities
+++++++++

+------------------------------------+------------------------------------------------------------+
| Function                           | Utility                                                    |
+====================================+============================================================+
| ``seqm.random_sequence``           | Generate random sequence.                                  |
+------------------------------------+------------------------------------------------------------+
| ``seqm.wrap``                      | Newline-wrap sequence                                      |
+------------------------------------+------------------------------------------------------------+


Questions/Feedback
==================

File an issue in the `GitHub issue tracker <https://github.com/atgtag/seqm/issues>`_.
