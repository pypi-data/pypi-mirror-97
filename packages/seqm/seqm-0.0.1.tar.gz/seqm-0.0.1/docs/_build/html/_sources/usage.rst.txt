=====
Usage
=====

Overview
========

The `seqm <http://atgtag.github.io/seqm/latest>`_ module contains functions for calculating sequence-related distance and complexity metrics, commonly used in language processing and next-generation sequencing. It has a simple and consistent API that be used for investigating sequence characteristics:

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


It also has a :class:`seqm.Sequence` object for object-based access to these properties:

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


All of the metrics available in the repository are listed below, and can also be found in the `API <./api.html>`_ section of the documentation.


List of Available Functions
===========================

.. currentmodule:: seqm

Sequence Quantification
-----------------------

+---------------------------------+------------------------------------------------------------+
| Function                        | Metric                                                     |
+=================================+============================================================+
| :func:`polydict`                | Length of longest homopolymer for all bases in sequence.   |
+---------------------------------+------------------------------------------------------------+
| :func:`polylength`              | Length of longest homopolymer in sequence.                 |
+---------------------------------+------------------------------------------------------------+
| :func:`entropy`                 | Shannon entropy for bases in sequence.                     |
+---------------------------------+------------------------------------------------------------+
| :func:`gc_percent`              | Percentage of GC bases in sequence relative to all bases.  |
+---------------------------------+------------------------------------------------------------+
| :func:`gc_skew`                 | GC skew for sequence:  (#G - #C)/(#G + #C).                |
+---------------------------------+------------------------------------------------------------+
| :func:`gc_shift`                | GC shift for sequence: (#A + #T)/(#G + #C)                 |
+---------------------------------+------------------------------------------------------------+
| :func:`dna_weight`              | Molecular weight for sequence with DNA backbone.           |
+---------------------------------+------------------------------------------------------------+
| :func:`rna_weight`              | Molecular weight for sequence with RNA backbone.           |
+---------------------------------+------------------------------------------------------------+
| :func:`aa_weight`               | Molecular weight for amino acid sequence.                  |
+---------------------------------+------------------------------------------------------------+
| :func:`zipsize`                 | Compressibility of sequence.                               |
+---------------------------------+------------------------------------------------------------+


Domain Conversion
-----------------

+---------------------------------+------------------------------------------------------------+
| Function                        | Conversion                                                 |
+=================================+============================================================+
| :func:`revcomplement`           | Length of longest homopolymer for all bases in sequence.   |
+---------------------------------+------------------------------------------------------------+
| :func:`complement`              | Length of longest homopolymer in sequence.                 |
+---------------------------------+------------------------------------------------------------+
| :func:`aa`                      | Shannon entropy for bases in sequence.                     |
+---------------------------------+------------------------------------------------------------+
| :func:`wrap`                    | Percentage of GC bases in sequence relative to all bases.  |
+---------------------------------+------------------------------------------------------------+
| :func:`likelihood`              | GC skew for sequence:  (#G - #C)/(#G + #C).                |
+---------------------------------+------------------------------------------------------------+
| :func:`qscore`                  | GC shift for sequence: (#A + #T)/(#G + #C)                 |
+---------------------------------+------------------------------------------------------------+


Distance Metrics
----------------

+---------------------------------+------------------------------------------------------------+
| Function                        | Distance Metric                                            |
+=================================+============================================================+
| :func:`hamming`                 | Hamming distance between sequences.                        |
+---------------------------------+------------------------------------------------------------+
| :func:`edit`                    | Edit (levenshtein) distance between sequences              |
+---------------------------------+------------------------------------------------------------+


Utilities
---------

+------------------------------------+------------------------------------------------------------+
| Function                           | Utility                                                    |
+====================================+============================================================+
| :func:`random_sequence`            | Generate random sequence.                                  |
+------------------------------------+------------------------------------------------------------+
| :func:`wrap`                       | Newline-wrap sequence                                      |
+------------------------------------+------------------------------------------------------------+


Command-Line Usage
==================

Once seqm is installed, all methods can be accessed via the ``seqm`` entry point:

.. code-block:: bash

    ~$ seqm


To run a specific method on a sequence, use:

.. code-block:: bash

    ~$ seqm gc_skew AGTAGTAGTTTAGGTTAGGTAG
    8.0


For commands comparing sequences, simply use both sequences as arguments:

.. code-block:: bash

    ~$ seqm edit AGTAGTAGTAGTAT AGTAGTAGTAGAAAAT
    3


And finally, to supply command line arguments to a method, do the following:

.. code-block:: bash

    ~$ seqm wrap AGTAGTAGTAGTATAGTAGTAGTAGAAAAT bases=10
    AGTAGTAGTA
    GTATAGTAGT
    AGTAGAAAAT
