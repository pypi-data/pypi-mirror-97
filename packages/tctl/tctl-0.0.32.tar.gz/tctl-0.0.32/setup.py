#!/usr/bin/env python

from setuptools import setup, find_packages
from codecs import open
from os import path

# --- get version ---
version = "unknown"
with open("tctl/version.py") as f:
    line = f.read().strip()
    version = line.replace("version = ", "").replace('"', '')
# --- /get version ---

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
long_description = "Tradologics CLI"
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()
if long_description == "Tradologics CLI":
    with open(path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = f.read()

req_file = 'requirements.txt'
with open(req_file, encoding="utf-8") as f:
    requirements = [line.rstrip() for line in f]

# ----------------------------------------

setup(
    name="tctl",
    version=version,
    description="Tradologics Command-line Utility",
    long_description=long_description,
    url="https://tradologics.com/tctl",
    author="Tradologics, Inc.",
    author_email="opensource@tradologics.com",
    license="Apache 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 4 - Beta",

        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",

        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    platforms=["any"],
    keywords="tradologics, tradologics.com",
    packages=find_packages(exclude=["contrib", "docs", "tests", "examples"]),
    install_requires=requirements,

    py_modules=["tctl"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "tctl=tctl:cli",
        ],
    },
)
