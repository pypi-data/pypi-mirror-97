from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pna-finder',
    version='0.2',
    author='Thomas Aunins',
    author_email='',
    description='A toolbox for identifying PNA antisense sequences',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/taunins/pna_finder',
    license='GNU LGPLv3',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    python_requires='>=2.7',
    install_requires=[
        'gffutils',
        'biopython'
    ]

)
