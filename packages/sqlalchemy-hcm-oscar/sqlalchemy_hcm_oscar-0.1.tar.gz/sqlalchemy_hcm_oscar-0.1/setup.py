#!/usr/bin/env python
"""
Setup for SQLAlchemy backend for DM
"""
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_params = dict(
    name="sqlalchemy_hcm_oscar",
    version='0.1',
    description="SQLAlchemy dialect for oscar special for hcm",
    author="tangrj",
    author_email="tangrj@inspur.com",
    keywords='oscar hcm SQLAlchemy',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "sqlalchemy.dialects":
            ["oscar = sqlalchemy_oscar.stpython:OracleDialect_stpython", "oscar.stpython = sqlalchemy_oscar.stpython:OracleDialect_stpython"]
    },
    install_requires=['sqlalchemy'],
)

if __name__ == '__main__':
    setup(**setup_params)
