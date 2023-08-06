#!/usr/bin/env python
from pathlib import Path

from setuptools import setup


def get_version():
    ini_path = Path(__file__).parent / "ozark" / "__init__.py"
    for line in ini_path.open():
        if line.startswith("__version__"):
            return line.split("=")[1].strip("' \"\n")
    raise ValueError(f"__version__ line not found in {ini_path}")


long_description = """
Ozark is a command-line utility that deploys Python scripts as batch
jobs on AWS Lambda.

Ozark abstract configuration and environment, handle code deployment,
layers and scheduling.
"""

description = "Ozark deploys your Python scripts on Lambda."

setup(
    name="ozark",
    version=get_version(),
    description=description,
    long_description=long_description,
    author="Bertrand Chenal",
    url="https://github.com/bertrandchenal/ozark",
    license="MIT",
    packages=["ozark"],
    install_requires=[
        "omegaconf",
        "boto3",
        "dateparser"
    ],
    entry_points={
        "console_scripts": [
            "ozark = ozark.cli:main",
        ],
    },
)
