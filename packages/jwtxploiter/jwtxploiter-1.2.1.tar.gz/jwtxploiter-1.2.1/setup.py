#!/usr/bin/python3

import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="jwtxploiter",
    version="1.2.1",
    author="Andrea Tedeschi",
    author_email="andrea.tedeschi@andreatedeschi.uno",
    description="A cli tool to test security of JSON Web Token",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPL-3.0",
    url="https://github.com/DontPanicO/jwtXploiter",
    install_requires=[
        "cryptography>=3.2.1"
    ],
    python_requires=">=3.7",
    platforms='posix',
    scripts=["bin/jwtxpl"],
)
