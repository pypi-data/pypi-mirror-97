#!/usr/bin/env python
"""
    Python Setup for 'muld'
"""
import codecs
import glob
import os
import setuptools


def read(*parts):
    """Read parts to use a e.g. long_description"""

    here = os.path.abspath(os.path.dirname(__file__))

    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, *parts), 'r') as pfp:
        return pfp.read()


setuptools.setup(
    name="muld",
    version="0.0.10",
    description="git; Mirror from Upstream to Local to Downstream",
    long_description=read('README.rst'),
    author="Simon A. F. Lund",
    author_email="os@safl.dk",
    url="https://github.com/safl/muld",
    license="Apache License 2.0",
    install_requires=[
        "pyyaml (>=3.10)"
    ],
    zip_safe=False,
    data_files=[
        ("bin", glob.glob("bin/*")),
    ],
    options={'bdist_wheel': {'universal': True}},
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
)
