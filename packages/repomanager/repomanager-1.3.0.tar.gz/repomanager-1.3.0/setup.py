import os
import codecs
import pip
from setuptools import setup, find_packages

import repomanager

# Base directory of package
here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


#Long Description
with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(name="repomanager",
    version=repomanager.__version__,
    description="Git Repository Manager",
    long_description=long_description,
    classifiers=[
          "Programming Language :: Python :: 3.6",
          "License :: OSI Approved :: BSD License",
          "Development Status :: 4 - Beta"
    ],
    url='https://gitlab.com/incoresemi/utils/repomanager',
    author='InCore Semiconductors Pvt. Ltd.',
    author_email='info@incoresemi.com',
    license='BSD-3-Clause',
    packages=find_packages(),
    keywords='repomanager',
    test_suite='tests',
    zip_safe=False,
    entry_points={
        'console_scripts': ['repomanager=repomanager.main:main'],
    })
