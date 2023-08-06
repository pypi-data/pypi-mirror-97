#!/usr/bin/env python3
"""Setup file for pysimmods package."""
import os
import setuptools


with open("VERSION") as freader:
    VERSION = freader.readline().strip()


with open("README.md") as freader:
    README = freader.read()


setuptools.setup(
    name="pysimmods",
    version=VERSION,
    author="Stephan Balduin",
    author_email="stephan.balduin@offis.de",
    description="A set of simulation models representing different "
    "distributed consumer or generator units.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/midas-mosaik/pysimmods",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=["numpy<=1.19.3", "pandas"],
    license="LGPL",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v2 (LGPLv2)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
)
