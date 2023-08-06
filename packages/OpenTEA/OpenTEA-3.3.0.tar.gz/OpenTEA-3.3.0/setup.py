#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
    Nested object manipulations OPENTEA

"""

from glob import glob
from os.path import basename
from os import path
#from os.path import splitext
from setuptools import find_packages, setup

NAME = "OpenTEA"

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(this_directory, 'VERSION'), encoding='utf-8') as f:
    version = f.read()

setup(
    name=NAME,
    version=version,
    description='Graphical User Interface engine based upon Schema',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["GUI", "SCHEMA", "Tkinter"],
    author="Antoine Dauptain, Aimad Er-raiy",
    author_email="coop@cerfacs.fr",
    url="http://cerfacs.fr/coop/",
    license="CeCILL-B",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[path.splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            "opentea3 = opentea.cli:main_cli",
        ],
    },
    install_requires=[
        'numpy>=1.16.2',
        'h5py>=2.6.0',
        'jsonschema',
        'markdown',
        'Pillow>=5.4.1',
        'PyYAML>=3.13',
        'nob>=0.4.1',
        'nobvisual',
        'requests',
        'click',
        'tiny_3d_engine>=0.2'
    ],
)
