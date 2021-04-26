#!/usr/bin/env python

PROJECT = 'virtualenvwrapper_ctf'
VERSION = '0.0.3'

# Bootstrap installation of Distribute
from setuptools import setup, find_packages

setup(
    name=PROJECT,
    version=VERSION,
    platforms=['Any'],
    provides=['virtualenvwrapper_ctf'],
    install_requires=[
        'virtualenv',
        'virtualenvwrapper',
        'requests>=2.25.1',
        'pandas>=1.2.4',
    ],
    namespace_packages=['vctf'],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'virtualenvwrapper.project.template': [
            'ctf = vctf.__init__:template',
        ],
        'console_scripts': [
            'vctf=vctf.__main__:main',
        ],
    },
    scripts=[
        'scripts/startctf',
    ]
)
