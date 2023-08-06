#!/usr/bin/env python

import os
from setuptools import setup, find_packages

here = os.path.dirname(os.path.abspath(__file__))

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version_ns = {}
with open(os.path.join(here, 'geedatasets', '_version.py')) as f:
    exec(f.read(), {}, version_ns)

# the setup
setup(
    name='geedatasets',
    version=version_ns['__version__'],
    description='Google Earth Engine Datasets coded in Python for easier manipulation',
    long_description='',
    url='',
    author='Rodrigo E. Principe',
    author_email='fitoprincipe82@gmail.com',
    license='MIT',
    keywords='google earth engine raster image processing gis satellite',
    packages=find_packages(exclude=('docs', 'js')),
    include_package_data=True,
    install_requires=['geetools'],
    extras_require={
    'dev': [],
    'docs': [],
    'testing': [],
    },
    classifiers=['Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'License :: OSI Approved :: MIT License',],
    )
