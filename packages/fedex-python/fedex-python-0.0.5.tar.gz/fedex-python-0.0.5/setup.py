#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Copyright 2020 fedex-python
# Author: Sergio Alvarado (sergioal18v@gmail.com)
# =============================================================================

# -----------------------------------------------------------------------------
# Libraries
# -----------------------------------------------------------------------------
# Core libs

# Third party libs
import setuptools

# Project libs
# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Main code
# -----------------------------------------------------------------------------
with open("README.md", "r") as fh:
    long_description = fh.read()
    print(long_description)

setuptools.setup(
    name='fedex-python',
    version='0.0.5',
    description='NOT official module for use fedex web services with python',
    description_content_type="text/plain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sr1871/fedex-python",
    author='Sergio Alvarado',
    author_email='sergioal18v@gmail.com',
    packages=setuptools.find_packages(),
    install_requires=['zeep>=3.4.0', 'pydantic>=1.6.1'],
    package_data={'fedex_python': ['wsdl/*.wsdl', 'wsdl/test/*.wsdl']},
    keywords=['FedEx', 'python'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)