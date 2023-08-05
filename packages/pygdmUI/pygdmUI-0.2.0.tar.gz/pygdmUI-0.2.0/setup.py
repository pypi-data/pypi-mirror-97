from __future__ import print_function
from __future__ import absolute_import

import os
import re

from setuptools import setup
# from numpy.distutils.core import setup
# from numpy.distutils.core import Extension
#from numpy.distutils.misc_util import Configuration

#from . import __name__, __version__, __author__

def read_version_file(*parts):
    return open(os.path.join(*parts), 'r').read()

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def find_version(*file_paths):
    version_file = read_version_file(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

def find_name(*file_paths):
    version_file = read_version_file(*file_paths)
    version_match = re.search(r"^__name__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find name string.")

def find_author(*file_paths):
    version_file = read_version_file(*file_paths)
    version_match = re.search(r"^__author__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find author string.")


print ("\n" + 60*'#' + "\n")

setup(
    name = find_name("pygdmUI", "__init__.py"),
    version = find_version("pygdmUI", "__init__.py"),
    author = find_author("pygdmUI", "__init__.py"),
    author_email = "pwiecha@laas.fr",
    description = ("A python full-field electrodynamical solver, "
                   "based on the Green dyadic method (volume integral technique "
                   "in frequency domain)."),
    license = "GPLv3+",
    long_description=read('README.rst'),
    packages=['pygdmUI'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Scientific/Engineering :: Physics",
        "Environment :: Console",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience :: Science/Research"
    ],
    url = 'https://gitlab.com/wiechapeter/pygdm-ui',
    download_url = '',
    keywords = ['coupled dipoles method', 'green dyadic method', 'electrodynamical simulations', 'nano optics', 'frequency-domain'],
    install_requires=['pyGDM2', 'numpy', 'mayavi', 'matplotlib', 'pyQt5'],
    python_requires='>=3.5',
) 
