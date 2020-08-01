#!/usr/bin/env python

PROJECT = 'virtualenvwrapper_ctf'
VERSION = '0.0.2'

# Bootstrap installation of Distribute
from setuptools import setup,  find_packages

setup(
    name=PROJECT,
    version=VERSION,
    platforms=['Any'],
    provides=['virtualenvwrapper_ctf'],
    requires=['virtualenv', 'virtualenvwrapper'],
    namespace_packages=['virtualenvwrapper'],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'virtualenvwrapper.project.template': [
            'ctf = virtualenvwrapper.ctf:template',
        ],
    },
    scripts=[
        'scripts/active_ctf.sh',
        'scripts/addchallenge',
        'scripts/initctf',
        'scripts/startctf',
        'scripts/endctf',
    ]
)
