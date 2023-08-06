#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Package setup
#
# ------------------------------------------------


# imports
# -------
import re
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


# config
# ------
class Config:
    def __init__(self, fi):
        with open(fi) as meta:
            for m in re.findall(r'(__[a-z]+__).*=.*[\'"](.+)[\'"]', meta.read()):
                setattr(self, m[0], m[1])
        return


pkgs = find_packages(exclude=['tests', 'docs', '*.egg.info'])
config = Config('{}/__init__.py'.format(pkgs[0]))


# requirements
# ------------
with open('requirements.txt', 'r') as reqs:
    requirements = list(map(lambda x: x.rstrip(), reqs.readlines()))

test_requirements = [
    'pytest',
    'pytest-cov',
    'pytest-runner'
]


# readme
# ------
with open('README.rst') as readme_file:
    readme = readme_file.read()


# exec
# ----
setup(
    name=config.__pkg__,
    version=config.__version__,
    description=config.__info__,
    long_description=readme,
    author=config.__author__,
    author_email=config.__email__,
    url=config.__url__,
    packages=pkgs,
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords=[config.__pkg__, 'seq', 'sequence', 'metrics', 'ngs', 'sequencing', 'distance', 'hamming', 'edit'],
    entry_points={
        'console_scripts': [
            '{} = {}.__main__:main'.format(config.__pkg__, config.__pkg__)
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apple Public Source License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    tests_require=test_requirements
)
