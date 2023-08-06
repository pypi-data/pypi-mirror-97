# -*- coding: utf-8 -*-
#
# Testing for package entry points
#
# ------------------------------------------------


# imporobj
# -------
import subprocess

from seqm import __version__, __pkg__
from . import BASE


# session
# -------
class TestEntryPoints:

    def call(self, subcommand, *args):
        return subprocess.check_output('python -m {} {} {}'.format(
            __pkg__, subcommand, ' '.join(args)
        ), stderr=subprocess.STDOUT, shell=True, cwd=BASE).decode().rstrip()

    def test_version(self):
        res = self.call('-v')
        assert res == __version__
        return

    def test_metric(self):
        res = self.call('length ATGTAG')
        assert res == str(6)
        return

    def test_distance(self):
        res = self.call('hamming ATGTAG ATATTG')
        assert res == str(2)
        return

    def test_conversion(self):
        res = self.call('aa ATGGAT')
        assert res == 'MD'
        return

    def test_utils(self):
        res = self.call('random --length 10')
        assert len(res) == 10
        return
