import logging
import os
from datetime import datetime

from setuptools import find_packages, setup

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = []

setup(
    name="profilerpy",
    version=0.2,
    author="Taher Rahgooy",
    author_email="taher.rahgooy@gmail.com",
    description="A simple code profiling library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rahgooy/profiler",
    python_requires=">=3",
    packages=['profilerpy'],
    license="",
    install_requires=install_requires,
    extras_require={
    },
)