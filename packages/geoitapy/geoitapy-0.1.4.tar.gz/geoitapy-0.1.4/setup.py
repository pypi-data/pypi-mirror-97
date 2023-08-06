import os

import setuptools
import sys

from configparser import ConfigParser

config: ConfigParser = ConfigParser()
config_path = '../geoitapy/.geoitapy.conf'
config.read(config_path)

ap = config.getboolean('pypi', 'upload')
at = config.getboolean('testpypi', 'upload')

if ap:
    VERSION = config.get('pypi', 'version')
elif at:
    VERSION = config.get('testpypi', 'version')
else:
    raise RuntimeError('LOSE')

with open("README.md", "r") as fh:
    long_description = fh.read()

CLASSIFIERS = """\
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Topic :: Software Development
Operating System :: OS Independent
Operating System :: POSIX
Operating System :: Unix
Development Status :: 1 - Planning
"""

setuptools.setup(
    name="geoitapy",
    version=VERSION,
    author="Mattia Sanchioni",
    author_email="mattia.sanchioni.dev@gmail.com",
    description="Python Geocoding Toolbox for Italy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mett96/geoitapy",
    packages=setuptools.find_packages(),
    install_requires=[
        'loggerpy',
        'pandas',
        'numpy',
    ],
    classifiers=[_f for _f in CLASSIFIERS.split("\n") if _f],
    python_requires='>=3.6',
)
