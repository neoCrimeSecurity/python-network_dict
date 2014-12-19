#!/usr/bin/env python
from os.path import exists
from setuptools import setup

if exists('README.rst'):
    desc = open('README.rst').read()
else:
    desc = ''

with open('requirements.txt') as f:
        required = f.read().splitlines()

setup(
    name                =   'network_dict',
    version             =   '0.1',
    packages            =   ['network_dict'],
    license             =   'LGPLv2.1',
    description         =   'network_dict creates a network subnet based dictionary that returns the most specific subnet(s) for a given IP.',
    author              =   'Michael Henry a.k.a. neoCrimeLabs',
    author_email        =   'mhenry@neocri.me',
    url                 =   'https://github.com/neoCrimeLabs/python-network_dict',
    long_description    =   desc,
    install_requires    =   required,
    classifiers         =   [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: System :: Networking']
    )