#!/usr/bin/env python3

import os
from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name="sandpiper-saas",
    version="0.9.0",
    author="Redwood EDA",
    description=(
        "Sandpiper SaaS"
    ),
    keywords="sandpiper tlv tl-verilog verilog rtl hdl compiler",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=['sandpiper'],
    classifiers = [
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={'console_scripts': ['sandpiper=sandpiper:run']},
    install_requires=['requests', 'argparse', 'click', 'Path']
)
