import setuptools

import codecs
import os.path

# versioning handled by the first method on:
# https://packaging.python.org/guides/single-sourcing-package-version/


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pugna",
    version=get_version("pugna/__init__.py"),
    author="Sebastian Khan",
    author_email="KhanS22@Cardiff.ac.uk",
    description="A lightweight package to perform regression with neural nets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/SpaceTimeKhantinuum/pugna",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
    scripts=[
        'bin/pugna_fit',
        'bin/pugna_scale_data'
    ]
)
