# -*- coding: utf-8 -*-
#
#    Copyright 2020 Ibai Roman
#
#    This file is part of EvoCov.
#
#    EvoCov is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    EvoCov is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with EvoCov. If not, see <http://www.gnu.org/licenses/>.

import os.path
import setuptools


def read(file):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, file), 'r') as f:
        return f.read()


setuptools.setup(
    name='evocov',
    version='0.0.10',
    author='Ibai Roman',
    author_email='ibaidev@protonmail.com',
    description='EvoCov extension to learn the kernel function.',
    license='GPLv3',
    keywords='Kernel Learning',
    url='https://gitlab.com/ibaidev/evocov',
    long_description=read('README.rst'),
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    install_requires=[
        'gplib',
        'numpy',
        'deap'
    ]
)
