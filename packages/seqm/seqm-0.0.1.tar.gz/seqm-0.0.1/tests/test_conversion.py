# -*- coding: utf-8 -*-


# imports
# -------
from parameterized import parameterized

import seqm as pkg


# tests
# -----
class TestConversion:

    @parameterized.expand((
        ('ACGT', 'ACGT'),
        ('AAAAAAAAAAA', 'TTTTTTTTTTT'),
        ('ATGACTGAATATAAACTTGT', 'ACAAGTTTATATTCAGTCAT'),
    ))
    def test_revcomplement(self, sequence, res):
        assert pkg.revcomplement(sequence) == res
        return

    @parameterized.expand((
        ('ACGT', 'TGCA'),
        ('AAAAAAAAAAA', 'TTTTTTTTTTT'),
        ('ATGACTGAATATAAACTTGT', 'TACTGACTTATATTTGAACA'),
    ))
    def test_complement(self, sequence, res):
        assert pkg.complement(sequence) == res
        return

    @parameterized.expand((
        ('ACGT', 'T'),
        ('GGGGGGGGGG', 'GGG'),
        ('ATGACTGAATATAAACTTGT', 'MTEYKL'),
    ))
    def test_aa(self, sequence, res):
        assert pkg.aa(sequence) == res
        return

    @parameterized.expand((
        ('*', [0.12589254117941673]),
        ('I@+', [0.0001, 0.0007943282347242813, 0.1]),
    ))
    def test_likelihood(self, sequence, res):
        assert pkg.likelihood(sequence) == res
        return

    @parameterized.expand((
        ('*', [9]),
        ('I@+', [40, 31, 10]),
    ))
    def test_qscore(self, sequence, res):
        assert pkg.qscore(sequence) == res
        return
