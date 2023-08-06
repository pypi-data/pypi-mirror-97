# -*- coding: utf-8 -*-

# config
__pkg__ = 'seqm'
__url__ = 'https://github.com/atgtag/seqm'
__info__ = 'Utilities for calculating sequence metrics.'
__author__ = 'Blake Printy'
__email__ = 'bprinty@gmail.com'
__version__ = '0.0.1'


# metrics
from .metrics import length
from .metrics import polydict
from .metrics import polylength
from .metrics import entropy
from .metrics import gc_percent
from .metrics import gc_skew
from .metrics import gc_shift
from .metrics import dna_weight
from .metrics import rna_weight
from .metrics import aa_weight
from .metrics import zipsize


# conversion
from .conversion import revcomplement
from .conversion import complement
from .conversion import aa
from .conversion import wrap
from .conversion import likelihood
from .conversion import qscore


# distance
from .distance import hamming
from .distance import edit


# utils
from .utils import random
from .utils import wrap


# objects
from .objects import Sequence
