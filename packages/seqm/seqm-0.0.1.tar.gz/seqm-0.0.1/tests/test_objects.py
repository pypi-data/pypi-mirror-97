# -*- coding: utf-8 -*-


# imports
# -------
from parameterized import parameterized

import seqm as pkg


# tests
# -----
class TestSequence:

    def test_properties(self):
        s = pkg.Sequence('ACGT')
        assert s.sequence == 'ACGT'
        return

    def test_operators(self):
        s1 = pkg.Sequence('ACGT')

        # add
        res = s1 + 'AAAA'
        assert res.sequence == 'ACGTAAAA'
        res = s1 + pkg.Sequence('AAAA')
        assert res == 'ACGTAAAA'

        # contains
        assert 'CG' in res
        assert 'AAA' in res
        assert 'AGAGAGAG' not in res

        # len
        assert len(res) == 8
        return

    @parameterized.expand((
        ('ACGT', 'ACGT'),
        ('AAAAAAAAAAA', 'TTTTTTTTTTT'),
        ('ATGACTGAATATAAACTTGT', 'ACAAGTTTATATTCAGTCAT'),
    ))
    def test_revcomplement(self, sequence, res):
        obj = pkg.Sequence(sequence)
        assert obj.revcomplement == res
        return

    @parameterized.expand((
        ('ACGT', 'TGCA'),
        ('AAAAAAAAAAA', 'TTTTTTTTTTT'),
        ('ATGACTGAATATAAACTTGT', 'TACTGACTTATATTTGAACA'),
    ))
    def test_complement(self, sequence, res):
        obj = pkg.Sequence(sequence)
        assert obj.complement == res
        return

    @parameterized.expand((
        ('ACGT', 'T'),
        ('GGGGGGGGGG', 'GGG'),
        ('ATGACTGAATATAAACTTGT', 'MTEYKL'),
    ))
    def test_aa(self, sequence, res):
        obj = pkg.Sequence(sequence)
        assert obj.aa == res
        return

    @parameterized.expand((
        ('ACGT', {'A': 1, 'C': 1, 'T': 1, 'G': 1}),
        ('AAAAAAAAAAA', {'A': 11, 'C': 0, 'T': 0, 'G': 0}),
        ('ATGACTGAATATAAACTTGT', {'A': 3, 'C': 1, 'T': 2, 'G': 1}),
    ))
    def test_polydict(self, sequence, res):
        obj = pkg.Sequence(sequence)
        assert obj.polydict == res
        return

    @parameterized.expand((
        ('ACGT', 1),
        ('AAAAAAAAAAA', 11),
        ('ATGACTGAATATAAACTTGT', 3),
    ))
    def test_polylength(self, sequence, res):
        obj = pkg.Sequence(sequence)
        assert obj.polylength == res
        return

    @parameterized.expand((
        ('ACGT', 2.0),
        ('AAAAAAAAAAA', 0),
        ('ATGACTGAATATAAACTTGT', 1.80),
    ))
    def test_entropy(self, sequence, res):
        obj = pkg.Sequence(sequence)
        assert round(obj.entropy, 2) == res
        return

    @parameterized.expand((
        ('ACGT', 0.5),
        ('AAAAAAAAAAA', 0),
        ('ATGACTGAATATAAACTTGT', 0.25),
    ))
    def test_gc_percent(self, sequence, res):
        obj = pkg.Sequence(sequence)
        assert obj.gc_percent == res
        return

    @parameterized.expand((
        ('ACGT', 0),
        ('AAAAAAAAAAA', 0.0),
        ('ATGACTGAATATAAACTTGT', 1.0),
    ))
    def test_gc_skew(self, sequence, res):
        obj = pkg.Sequence(sequence)
        assert obj.gc_skew == res
        return

    @parameterized.expand((
        ('ACGT', 1.0),
        ('AAAAAAAAAAA', 11.0),
        ('ATGACTGAATATAAACTTGT', 3.0),
    ))
    def test_gc_shift(self, sequence, res):
        obj = pkg.Sequence(sequence)
        assert obj.gc_shift == res
        return

    @parameterized.expand((
        ('ACGT', 1947.8),
        ('AAAAAAAAAAA', 5403.2),
        ('ATGACTGAATATAAACTTGT', 9761),
    ))
    def test_dna_weight(self, sequence, res):
        obj = pkg.Sequence(sequence)
        assert round(obj.dna_weight, 2) == res
        return

    @parameterized.expand((
        ('ACGT', 1997.8),
        ('AAAAAAAAAAA', 5579.2),
        ('ATGACTGAATATAAACTTGT', 9983.0),
    ))
    def test_rna_weight(self, sequence, res):
        obj = pkg.Sequence(sequence)
        assert round(obj.rna_weight, 2) == res
        return

    @parameterized.expand((
        ('ACGT', 404.5),
        ('AAAAAAAAAAA', 980.1),
        ('ATGACTGAATATAAACTTGT', 2014.2),
    ))
    def test_aa_weight(self, sequence, res):
        obj = pkg.Sequence(sequence)
        assert round(obj.aa_weight, 2) == res
        return

    @parameterized.expand((
        ('ACGT', 12),
        ('AAAAAAAAAAA', 11),
        ('ATGACTGAATATAAACTTGT', 23),
    ))
    def test_zipsize(self, sequence, res):
        obj = pkg.Sequence(sequence)
        assert obj.zipsize == res
        return

    @parameterized.expand((
        ('ACGT', 2, 'AC\nGT'),
        ('AAAAAAAAAAA', 3, 'AAA\nAAA\nAAA\nAA'),
    ))
    def test_wrap(self, sequence, bases, res):
        obj = pkg.Sequence(sequence)
        assert obj.wrap(bases=bases) == res
        return

    @parameterized.expand((
        ('ACGT', 'ACGT', 0),
        ('AAAAAAAAAAA', 'AAAAAAATAAA', 1),
        ('ATGACTGAATATAAACTTGT', 'ATGACTCATTATGAACTTGT', 3),
    ))
    def test_hamming(self, sequence, other, res):
        obj = pkg.Sequence(sequence)
        assert obj.hamming(other) == res
        return

    @parameterized.expand((
        ('ACGT', 'ATGT', 1),
        ('AAAAAAAAAAA', 'AAAAAATAA', 3),
        ('ATGACTGAATATAAACTTGT', 'ATGACTGAATTAGTAAAAACTTGT', 4),
    ))
    def test_edit(self, sequence, other, res):
        obj = pkg.Sequence(sequence)
        assert obj.edit(other) == res
        return
