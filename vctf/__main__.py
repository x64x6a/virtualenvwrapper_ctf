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

from vctf.vctf import init, get_ctf_config
from vctf.vctf import set_active


log = logging.getLogger(__name__)

def main():
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
        name = args.init
        config = get_ctf_config(name)
        init(config, name)
    elif args.start:
        name = args.start
        set_active(name)
    elif args.end:
        subprocess.check_call(['endctf'])

if __name__ == '__main__':
    main()
