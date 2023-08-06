# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(
    name='dataverk-gsm',
    version='0.0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
    install_requires=install_requires,
    # metadata to display on PyPI
    author="NAV IKT",
    description="GSM integration for dataverk",
    license="MIT",
    keywords="gsm dataverk",
    url="https://github.com/navikt"
)
