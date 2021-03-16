#!/usr/bin/env python

PROJECT = 'virtualenvwrapper_ctf'
VERSION = '0.0.3'

# Bootstrap installation of Distribute
from setuptools import setup,  find_packages

setup(
    name=PROJECT,
    version=VERSION,
    platforms=['Any'],
    provides=['virtualenvwrapper_ctf'],
    requires=['virtualenv', 'virtualenvwrapper'],
    namespace_packages=['vctf'],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'virtualenvwrapper.project.template': [
            'ctf = vctf.ctf:template',
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
