import re
import ast
import os

from setuptools import find_packages, setup
from setuptools.extension import Extension
from setuptools.command.build_ext import build_ext as _build_ext


class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())
# Dealing with Cython
USE_CYTHON = os.environ.get('USE_CYTHON', False)
ext = '.pyx' if USE_CYTHON else '.c'


classes = """
    Development Status :: 0 - pre-alpha
    License :: OSI Approved :: BSD License
    Topic :: Software Development :: Libraries
    Topic :: Scientific/Engineering
    Topic :: Scientific/Engineering :: Bio-Informatics
    Programming Language :: Python :: 2
    Programming Language :: Python :: 2 :: Only
    Operating System :: Unix
    Operating System :: POSIX
    Operating System :: MacOS :: MacOS X
"""
classifiers = [s.strip() for s in classes.split('\n') if s]

description = ('Benchmarks')

with open('README.md') as f:
    long_description = f.read()


# version parsing from __init__ pulled from Flask's setup.py
# https://github.com/mitsuhiko/flask/blob/master/setup.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')

version  = "0.0.1"

setup(name='pba',
      version=version,
      license='BSD',
      description=description,
      long_description=long_description,
      author="Jamie Morton",
      author_email="jamietmorton@gmail.com",
      maintainer="Jamie Morton",
      maintainer_email="jamietmorton@gmail.com",
      packages=find_packages(),
      setup_requires=['numpy >= 1.9.2'],
      cmdclass={'build_ext': build_ext},
      install_requires=[
          'IPython >= 3.2.0',
          'matplotlib >= 1.4.3',
          'numpy >= 1.9.2',
          'pandas >= 0.18.0',
          'scipy >= 0.15.1',
          'nose >= 1.3.7',
          'scikit-bio > 0.5.0',
          'ete3',
          'biom-format'
      ],
      classifiers=classifiers,
      package_data={
          }
      )
