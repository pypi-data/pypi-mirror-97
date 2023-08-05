import codecs
import os.path
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            return line.split('"')[1]
    else:
        raise RuntimeError("Unable to find version string.")

setuptools.setup(
    name="pyxeed",
    version=get_version("pyxeed/__init__.py"),
    author="Soral",
    author_email="soral@x-i-a.com",
    description="Xeed Core Module Python Version",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/X-I-A/pyxeed",
    packages=setuptools.find_packages(),
    install_requires=[
        'xialib',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)