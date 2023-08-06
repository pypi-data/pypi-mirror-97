#!/usr/bin/env python
# Filename: setup.py
"""
The km3py setup script.

"""
from setuptools import setup


try:
    with open("README.rst") as fh:
        long_description = fh.read()
except UnicodeDecodeError:
    long_description = "The km3py metaproject is a collection of KM3NeT Python packages."


setup(
    name='km3py',
    url='https://git.km3net.de/km3py/km3py',
    description='The km3py metaproject is a collection of KM3NeT Python packages.',
    long_description=long_description,
    author='Tamas Gal',
    author_email='tgal@km3net.de',
    packages=['km3py'],
    include_package_data=True,
    platforms='any',
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    python_requires='>=3.6',
    install_requires=open("requirements.txt").readlines(),
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
    ],
)
