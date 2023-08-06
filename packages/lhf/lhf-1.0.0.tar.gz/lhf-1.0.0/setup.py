import setuptools
import os
import re
import sys
import sysconfig
import platform
import subprocess

from distutils.version import LooseVersion
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext

# class build_ext(_build_ext):
#     def finalize_options(self):
#         _build_ext.finalize_options(self)
#         # Prevent numpy from thinking it is still in its setup process:
#         __builtins__.__NUMPY_SETUP__ = False
#         import numpy
#         self.include_dirs.append(numpy.get_include())


setup(
    name='lhf',
    version='1.0.0',    
    description='Light Weight Homology Framework',
    project_urls={
        "LHF": "https://github.com/wilseypa/lhf",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    package_data={'libLHF': ['libLHFlib.so',
                          'libLHFlib.so.1',
                          'libLHFlib.so.1.0.0']},
    include_package_data=True,
)
