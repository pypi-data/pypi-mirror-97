# -*- coding: utf-8 -*-


# imports
# -------
from parameterized import parameterized

import seqm as pkg


# tests
# -----
class TestUtils:

    @parameterized.expand((
        (20, 'AC'),
        (5, 'ACGT'),
    ))
    def test_random(self, slen, tmpl):
        rs = pkg.random(slen, tmpl)
        assert len(rs) == slen
        return

    @parameterized.expand((
        ('ACGT', 2, 'AC\nGT'),
        ('AAAAAAAAAAA', 3, 'AAA\nAAA\nAAA\nAA'),
    ))
    def test_wrap(self, sequence, bases, res):
        wrp = pkg.wrap(sequence, bases=bases)
        assert wrp == res
        return
