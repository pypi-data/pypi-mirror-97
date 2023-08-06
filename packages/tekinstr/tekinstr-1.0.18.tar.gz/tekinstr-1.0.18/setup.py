"""Setuptools install script"""
from setuptools import setup, find_packages


def get_readme():
    """Get readme contents"""
    with open("README.md") as f:
        return f.read()


def get_version():
    """Get the version number"""
    with open("tekinstr/version.py") as f:
        lines = f.readlines()
    line = ""
    for line in lines:
        if line.startswith("__version__"):
            break
    version = [s.strip().strip('"') for s in line.split("=")][1]
    return version


setup(
    name="tekinstr",
    version=get_version(),
    author="Lee Johnston",
    author_email="lee.johnston.100@gmail.com",
    description="Communication with Tektronix oscilloscopes",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
    ],
    url="https://github.com/l-johnston/tekinstr",
    install_requires=["numpy", "sympy", "matplotlib", "unyt", "pyvisa"],
)
