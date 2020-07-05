
from os import path
from pathlib import Path
from subprocess import check_output

from setuptools import find_packages, setup

cwd = path.abspath(path.dirname(__file__))

with open(path.join(cwd, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

COMMIT_COUNT = "172"

MAJOR = COMMIT_COUNT[0] if len(COMMIT_COUNT) > 0 else 0
MINOR = COMMIT_COUNT[1] if len(COMMIT_COUNT) > 1 else 0

setup(
    name='pytsp',
    version=f'{MAJOR}.{MINOR}',

    packages=find_packages(),

    install_requires=[
        'matplotlib~=3.2.1',
        'click~=7.1.2'
    ],

    author='Vasileios Sioros',
    author_email='billsioros97@gmail.com',

    description='The Travelling Salesman Problem in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',

    keywords='tsp tsptw travelling salesman time windows vrp vechicle routing problem cli command line interface',

    project_urls={
        'Bug Tracker': 'https://github.com/billsioros/computational-geometry',
        'Documentation': 'https://github.com/billsioros/computational-geometry',
        'Source Code': 'https://github.com/billsioros/computational-geometry',
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
