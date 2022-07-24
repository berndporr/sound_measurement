#!/usr/bin/python3

from setuptools import setup

with open('README_py.rst') as f:
    long_description = f.read()

setup(
    name='sound_weighting_filters',
    version='0.9.3',
    description="IIR coefficients for A,B,C and ITU_R_468 weighting filters",
    long_description=long_description,
    author='Bernd Porr',
    author_email='mail@berndporr.me.uk',
    py_modules=['ABC_weighting','ITU_R_468_weighting'],
    zip_safe=False,
    url='https://github.com/berndporr/sound_weighting_filters',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
)
