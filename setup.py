# -*- coding: utf-8 -*-

import os
import re
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from pip.req import parse_requirements


TEST_REQUIRES = [
    'pytest',
    'responses',
]


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--verbose'
        ]
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.

    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version

__version__ = find_version('betfair_pandas/__init__.py')


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content

setup(
    name='betfair_pandas',
    version=__version__,
    description='Pandas adapter for betfair.py '
                '(https://api.developer.betfair.com/)',
    long_description=open('README.md').read(),
    author='Craig Tait',
    author_email='taitcraigd@gmail.com',
    url='https://github.com/cdtait/betfair_pandas',
    packages=find_packages(exclude=('test*','sample*', )),
    package_dir={'betfair_pandas': 'betfair_pandas'},
    include_package_data=True,
    install_requires=[
        str(requirement.req)
        for requirement in parse_requirements('requirements.txt')
    ],
    license=read('LICENSE'),
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPLv2 License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=TEST_REQUIRES,
    cmdclass={'test': PyTest}
)
