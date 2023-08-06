#!/usr/bin/env python
#coding:utf-8
"""
  Author:  LPP --<Lpp1985@hotmail.com>
  Purpose: 
  Created: 2015/1/1
"""
from distutils.core  import setup
from setuptools import find_packages


import codecs
import os
import sys


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()
NAME = "MicroPipe"

DESCRIPTION = " A package for automated microbe bioinfomatics Analysis"

LONG_DESCRIPTION = read("README.txt")
KEYWORDS = "Pipeline Bioinfomatics"
AUTHOR = "Pengpeng Li"
AUTHOR_EMAIL = "409511038@qq.com"
VERSION = "0.2.12"

setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
		'Programming Language :: Python :: 2',
    ],
	url="https://github.com/lpp1985/lpp_Script",
    install_requires=[
        "requests",
        "pandas",
        "numpy",
		"poster",
		"Pillow",
		"sqlobject",
		"sqlalchemy",
		"redis",
		"termcolor",
		"pyWorkFlow",
                "html5lib",
                "XlsxWriter",
                "beautifulsoup4",
                "xlrd",
                "lpp"
		
		
        ],    
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,

    packages = find_packages(),
    include_package_data=True,
    zip_safe=True,
    scripts=[
	"MicroPipe/Scripts/Circula.py",
	"MicroPipe/Scripts/Draw_qc.py",
	"MicroPipe/Scripts/thu.py",
	"MicroPipe/Scripts/Download_reference.py",
	"MicroPipe/Micro_pipeline.py"	
		],


)
 
