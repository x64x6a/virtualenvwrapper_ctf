#!/usr/bin/env python
"""
Create CTF work directory with virtualenvwrapper
"""
import argparse
import inspect
import logging
import os
import subprocess
import sys


log = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog=(__package__ or __file__),
        description='Copy files into CTF work directory',
    )
    parser.add_argument('--add', '-a', dest='add', nargs=2, metavar=('category', 'challenge'),
        help='Add a challenge to the active CTF')
    parser.add_argument('--init', '-i', dest='init', metavar='ctf_name',
        help='Initialize CTF within $PROJECT_HOME directory with given name')
    parser.add_argument('--start', '-s', dest='start', metavar='ctf_name',
        help='Start and initialize CTF within $PROJECT_HOME directory with given name')
    parser.add_argument('--end', '-e', dest='end', action='store_true',
        help='End active CTF')

    args = parser.parse_args()

    if args.add:
        from .addchallenge import add_challenge
        category, name = args.add
        add_challenge(category, name)
    elif args.init:
        from .initctf import initctf
        ctf_name = args.init
        initctf(ctf_name)
    elif args.start:
        ctf_name = args.start
        subprocess.check_call(['startctf', ctf_name])
    elif args.end:
        subprocess.check_call(['endctf'])
