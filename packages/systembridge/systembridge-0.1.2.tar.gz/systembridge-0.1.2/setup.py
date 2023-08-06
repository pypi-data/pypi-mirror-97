#!/usr/bin/env python
import io

from setuptools import setup, find_packages

version = "0.1.2"

setup(
    name="systembridge",
    version=version,
    description="Python package for connecting to System Bridge.",
    long_description=io.open("README.md", encoding="UTF-8").read(),
    keywords="system bridge connector",
    author="Aidan Timson (Timmo)",
    author_email="contact@timmo.xyz",
    url="https://github.com/timmo001/system-bridge-connector-py",
    packages=find_packages(exclude=["tests", "generator"]),
    install_requires=["aiohttp>=3.7.3"],
)
