#!/usr/bin/python3

from setuptools import setup

setup(
    name='sound_weighting_filters',
    version='0.9.0',
    description="IIR coefficients for A,B,C and ITU_R_468 weighting filters",
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
