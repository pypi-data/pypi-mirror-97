#!/usr/bin/env python
from setuptools import find_packages, setup

from taxi_clockify import __version__

with open("README.rst") as f:
    readme = f.read()

install_requires = [
    "requests>=2.3.0",
    "taxi~=6.0",
    "arrow>=0.15.8",
]

setup(
    name="taxi_clockify",
    version=__version__,
    packages=find_packages(),
    description="Taxi backend for clockify.me",
    long_description=readme,
    long_description_content_type="text/x-rst",
    author="Sylvain Fankhauser",
    author_email="sephi@fhtagn.top",
    url="https://github.com/sephii/taxi-clockify",
    install_requires=install_requires,
    license="wtfpl",
    python_requires=">=3.5",
    entry_points={"taxi.backends": "clockify = taxi_clockify.backend:ClockifyBackend",},
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
