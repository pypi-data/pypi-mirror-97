"""
Function for building the exergi package.

To build package use:
    python setup.py sdist bdist_wheel
To upload package to PyPi:
    twine upload dist/*
"""

import codecs
import os.path
import pathlib
from setuptools import find_packages, setup


def read(rel_path: str):
    """Read file in rel_path.

    Reads the file for the get_version function defined below. This function is
    only used in order to single source package version. Taken from guide:
    https://packaging.python.org/guides/single-sourcing-package-version/

    Args:
        rel_path (str): - Relative file to __init__.py file where version can
                          be found.
    Returns:
        file_p.read()   - Line in file.
        
    """
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as file_p:
        return file_p.read()


def get_version(rel_path: str) -> str:
    """Find version from line in rel_path.

    Args:
        rel_path (str): - Relative file to __init__.py file where version can
                          be found.

    Raises:
        RuntimeError:   - Error if version can be found in passed path.

    Returns:
        [type]: [description]
    """
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            version = line.split(delim)[1]
            break
    else:
        raise RuntimeError("Unable to find version string.")
    return version


HERE = pathlib.Path(__file__).parent  # The directory containing this file
README = (HERE / "README.md").read_text()  # The text of the README file

links = []
requires = []

# This call to setup() does all the work
setup(
    name="exergi",
    version=get_version("exergi/__init__.py"),
    description="SE Libary for various tasks",
    long_description=README,
    long_description_content_type="text/markdown",
    author="KasperJanehag",
    author_email="kasper.janehag@gmail.com",
    license="MIT",
    classifiers=["License :: OSI Approved :: MIT License",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.7"],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["pandas>=1.1.1",
                      "boto3>=1.14.15",
                      "tables",
                      "numpy>=1.19.0",
                      "psycopg2-binary",
                      "sqlalchemy",
                      "plotly",
                      "h5py",
                      "s3fs",
                      "colorama"
                      ],
)
