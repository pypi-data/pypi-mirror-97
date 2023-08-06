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
    version='0.9.2',    
    description='demo',
    #packages=['lhf'],
    packages=setuptools.find_packages(),
    #install_requires=['numpy',
    #                  'wheel'],
    package_data={'libLHF': ['libLHFlib.so',
                          'libLHFlib.so.1',
                          'libLHFlib.so.1.0.0']},
    include_package_data=True,
    # cmdclass={'build_ext':build_ext},
    # setup_requires=['numpy'],
)
