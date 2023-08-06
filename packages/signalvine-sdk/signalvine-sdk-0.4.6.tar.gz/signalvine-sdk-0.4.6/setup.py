#!/usr/bin/env python

from os.path import basename, splitext
from glob import glob
import pathlib

from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
from os.path import isfile

from setuptools import find_packages
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Pull requirements from the text file
requirement_path = HERE / "requirements.txt"
install_requires = []
if isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

# This call to setup() does all the work
setup(
    name="signalvine-sdk",
    version="0.4.6",
    description="SignalVine API SDK",
    long_description=README,
    long_description_content_type="text/markdown",
    author="CU Boulder, OIT",
    author_email="stta9820@colorado.edu",
    license="Apache License 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    url="https://github.com/CUBoulder-OIT/signalvine-sdk",
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
