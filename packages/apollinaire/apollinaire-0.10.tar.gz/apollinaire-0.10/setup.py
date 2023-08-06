#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Inspired by:
# https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
 
import codecs
import os
from setuptools import setup, find_packages
import re

NAME = 'apollinaire'
META_PATH = os.path.join ("apollinaire", "__init__.py")
PACKAGES = find_packages (where='.')
INSTALL_REQUIRES = ['numpy', 'pandas', 'numdifftools', 'statsmodels',
                    'emcee', 'dill', 'pathos', 'corner', 'h5py', 'scipy', 'urllib3',
                    'joblib', 'numba', 'george', 'astropy']
KEYWORDS = ["asteroseismology", "helioseismology", "bayesian", "peakbagging", "mcmc",
            "data", "data_analysis"]

##########################################################

HERE = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
        META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


if __name__ == "__main__":
    setup(
        name=NAME,
        description=find_meta("description"),
        license=find_meta("license"),
        url=find_meta("uri"),
        version=find_meta("version"),
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        keywords=KEYWORDS,
        packages=PACKAGES,
        include_package_data=True,
        zip_safe=False,
        install_requires=INSTALL_REQUIRES,
        options={"bdist_wheel": {"universal": "1"}},
    )
 
