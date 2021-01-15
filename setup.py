# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

with open("README.md") as file:
    readme = file.read()

with open("LICENSE") as file:
    license = file.read()


setup(
    name="category",
    version="0.1.0",
    description="Provide a functional programming library",
    long_description=readme,
    author="usabarashi",
    author_email="",
    url="https://github.com/usabarashi/python-category",
    license=license,
    packages=find_packages(exclude=("tests", "docs")),
    install_requires=[],
)
