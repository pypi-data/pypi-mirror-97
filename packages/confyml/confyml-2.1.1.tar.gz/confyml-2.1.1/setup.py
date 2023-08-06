import codecs
import os.path

from setuptools import find_packages, setup


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


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = get_version('confyml/__init__.py')

setup(
    name="confyml",
    version=version,
    author="iccyp",
    author_email='iccyp.py@gmail.com',
    description="Small package to apply YAML config to methods and functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iccyp/confyml",
    download_url='https://github.com/iccyp/confyml/archive/'
                 f'{version}.tar.gz',
    packages=find_packages(),
    install_requires=['PyYAML'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
