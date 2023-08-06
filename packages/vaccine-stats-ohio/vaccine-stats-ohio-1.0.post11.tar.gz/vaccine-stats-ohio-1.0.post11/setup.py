#!/usr/bin/env python

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    long_description = readme_file.read()

setup(
    name="vaccine-stats-ohio",
    version="1.0r11",
    description="Access and summarize Ohio COVID vaccine statistics",
    author="Eddie Cosma",
    author_email="vaxstat@eddiecosma.com",
    url="https://github.com/eddie-cosma/vaccine-stats-ohio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.6",
    include_package_data=True,
)
