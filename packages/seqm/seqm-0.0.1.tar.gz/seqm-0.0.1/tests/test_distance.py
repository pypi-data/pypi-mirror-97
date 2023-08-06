# -*- coding: utf-8 -*-


# imports
# -------
from parameterized import parameterized

import seqm as pkg


# tests
# -----
class TestDistance:

    @parameterized.expand((
        ('ACGT', 'ACGT', 0),
        ('AAAAAAAAAAA', 'AAAAAAATAAA', 1),
        ('ATGACTGAATATAAACTTGT', 'ATGACTCATTATGAACTTGT', 3),
    ))
    def test_hamming(self, sequence, other, res):
        assert pkg.hamming(sequence, other) == res
        return

    @parameterized.expand((
        ('ACGT', 'ATGT', 1),
        ('AAAAAAAAAAA', 'AAAAAATAA', 3),
        ('ATGACTGAATATAAACTTGT', 'ATGACTGAATTAGTAAAAACTTGT', 4),
    ))
    def test_edit(self, sequence, other, res):
        assert pkg.edit(sequence, other) == res
        return
