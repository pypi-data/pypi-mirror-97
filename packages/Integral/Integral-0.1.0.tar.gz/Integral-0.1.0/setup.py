# -*- coding: utf-8 -*-

import os
import re

from setuptools import find_packages
from setuptools import setup

# obtain version string from __init__.py
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'integral', '__init__.py'), 'r') as f:
    init_py = f.read()
version = re.search('__version__ = "(.*)"', init_py).groups()[0]

# obtain long description from README and CHANGES
README = '''
``BrainPy`` is a lightweight framework based on the latest Just-In-Time (JIT)
compilers (especially `Numba <https://numba.pydata.org/>`_).
The goal of ``BrainPy`` is to provide a unified simulation and analysis framework
for neuronal analysis with the feature of high flexibility and efficiency.
BrainPy is flexible because it endows the users with the fully data/logic flow control.
BrainPy is efficient because it supports JIT acceleration on CPUs and GPUs.
'''

# setup
setup(
    name='Integral',
    version=version,
    description='Integral: A backend-free numerical integration library for differential equations',
    long_description=README,
    author='Chaoming Wang',
    author_email='adaduo@outlook.com',
    packages=find_packages(exclude=['examples*', 'docs*', 'develop*', 'tests*']),
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.15',
        'numba>=0.50.0',
    ],
    url='https://github.com/PKU-NIP-Lab/BrainPy',
    keywords='computational neuroscience',
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries',
    ]
)
