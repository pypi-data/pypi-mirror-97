# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="adafruit-circuitpython-lsm9ds1",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="CircuitPython library for LSM9DS1 accelerometer, magnetometer, gyroscope.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    # The project's main homepage.
    url="https://github.com/adafruit/Adafruit_CircuitPython_LSM9DS1",
    # Author details
    author="Adafruit Industries",
    author_email="circuitpython@adafruit.com",
    install_requires=["Adafruit-Blinka", "adafruit-circuitpython-busdevice"],
    # Choose your license
    license="MIT",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    # What does your project relate to?
    keywords="adafruit accelerometer magnetometer gyroscope lsm9ds1"
    "breakout hardware micropython circuitpython",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    py_modules=["adafruit_lsm9ds1"],
)
