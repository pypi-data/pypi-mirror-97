"""Setup for package shapsplain
"""

from os import path
from setuptools import setup, find_packages

from shapsplain import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    name='shapsplain',
    version=__version__,
    author = 'BigML Team',
    author_email = 'team@bigml.com',
    url = 'http://bigml.com/',
    description='Wrapper for shapley explanations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=["tests", "tests.*"]),
    tests_require=[
        'nose>=1.3,<1.4',
        'bigml>=4.30,<4.31',
        'sensenet>=0.1.0,<0.2.0'
    ],
    test_suite='nose.collector',
    install_requires=[
        'numpy>=1.18,<1.19',
        'scikit-learn>=0.23,<0.24',
        'tensorflow>=2.3,<2.4',
        'numba>=0.50.1,<0.51.0'
    ])
