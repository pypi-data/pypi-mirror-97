#!/usr/bin/env python
# pylint: disable=C0103
import codecs
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
  user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

  def initialize_options(self):
    TestCommand.initialize_options(self)
    try:
      from multiprocessing import cpu_count

      self.pytest_args = ['-n', str(cpu_count()), '--boxed']
    except (ImportError, NotImplementedError):
      self.pytest_args = ['-n', '1', '--boxed']

  def finalize_options(self):
    TestCommand.finalize_options(self)
    self.test_args = []
    self.test_suite = True

  def run_tests(self):
    import pytest

    errno = pytest.main(self.pytest_args)
    sys.exit(errno)


requirements = codecs.open('./requirements.txt').read().splitlines()
long_description = codecs.open('./README.md').read()
version = codecs.open('./VERSION').read().strip()

test_requirements = [
  'pytest-cov',
  'pytest-mock',
  'pytest-xdist',
  'pytest',
]

setup(
  name='ltpylib',
  version=version,
  description='Common Python helper functions',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://github.com/lancethomps/ltpylib',
  project_urls={
    'Bug Reports': 'https://github.com/lancethomps/ltpylib/issues',
    'Source': 'https://github.com/lancethomps/ltpylib',
  },
  author='Lance Thompson',
  license='MIT',
  keywords='utils',
  python_requires='>=3.6',
  packages=['ltpylib', 'ltpylibtests'],
  install_requires=requirements,
  classifiers=[],
  cmdclass={
    'test': PyTest,
  },
  tests_require=test_requirements,
)
