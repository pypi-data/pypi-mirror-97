# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 09:27:00 2020

@author: Sangoi
"""
import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

    
setuptools.setup(
    name="ReferenceDataAccess", 
    version="0.0.10",
    author="Jay Sangoi",
    author_email="jay.sangoi@gmail.com",
    license='MIT',
    description='A python library to easily fetch reference data from RduAccess and integrate it with your python application',
    long_description=long_description,
    long_description_content_type='text/markdown',

    #url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Topic :: Office/Business :: Financial :: Investment',
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests'
    ],
    extras_requires={
        'pandas': ['pandas'],
    },
    python_requires='>=3.6',
    keywords=['stocks', 'market', 'finance', 'RduAccess', 'quotes', 'derivatives',
              'equity','fixed income','Mifid','shares','Reference Data'],
    
    include_package_data=True,
    package_data={'': ['*.csv']}
)    