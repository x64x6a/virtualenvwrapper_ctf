#!/usr/bin/env python
"""
Create CTF work directory with virtualenvwrapper
"""
import argparse
import logging
import os

from vctf import vctf
from vctf import ctf


log = logging.getLogger(__name__)

def get_name_or_active(args):
    if args.args is None or len(args.args) == 0:
        try:
            name = vctf.get_active()
        except FileNotFoundError:
            name = None
    else:
        name = args.args[0]
    return name

def main():
    parser = argparse.ArgumentParser(
        prog=(__package__ or __file__),
        description='Copy files into CTF work directory',
    )
    # base arguments
    parser.add_argument('command',
        help='Specify a command to run: init, start, end, add, list, pull, submit')
    parser.add_argument('args', nargs='*',
        help='[name] or [category challenge] or [challenge_id flag]')

    # customized arguments, can also set in .ini files
    parser.add_argument('--username', '-u')
    parser.add_argument('--password', '-p')
    parser.add_argument('--url', '-d', help='Root web URL')
    parser.add_argument('--platform', '-f', help='Hosting platform, supported: ' + ','.join(ctf.get_platforms()))
    parser.add_argument('--directory', help='CTF directory if not using default')
    parser.add_argument('--project_home', help='Directory if $PROJECT_HOME not used')
    parser.add_argument('--config', help='Config file if not using default')

    args = parser.parse_args()
    command = args.command

    # initialize a ctf, including directories and config file
    #   `init name [-u username] [-p password] [-d url] [-f platform]`
    if command == 'init' or command == 'i':
        if args.args is None or len(args.args) == 0:
            parser.error("the following arguments are required: args.  [name] not given")
        name = args.args[0]
        init_kwargs = {
            "username": args.username, "password": args.password,
            "url": args.url, "platform": args.platform,
            "directory": args.directory, "project_home": args.project_home
        }
        config = args.config if args.config else vctf.get_ctf_config(name)
        vctf.init(config, name, **init_kwargs)

    # start a ctf, setting it as active
    #   `start name`
    elif command == 'start' or command == 's':
        if args.args is None or len(args.args) == 0:
            parser.error("the following arguments are required: args.  [name] not given")
        name = args.args[0]
        vctf.set_active(name)

    # end active ctf
    #   `end`
    elif command == 'end' or command == 'e':
        vctf.end()

    # add a challenge manually for active ctf
    #   `add category challenge`
    elif command == 'add' or command == 'a':
        if args.args is None or len(args.args) < 2:
            parser.error("the following arguments are required: args.  [category challenge] not given")
        category = args.args[0]
        challenge = args.args[1]
        try:
            name = vctf.get_active()
        except FileNotFoundError:
            parser.error("active ctf not found")
        config = args.config if args.config else vctf.get_ctf_config(name)
        c = ctf.get_platform_object(config)
        c.add(category, challenge)

    # list challenges from ctf
    #   `list [name]`
    elif command == 'list' or command == 'l':
        name = get_name_or_active(args)
        if args.args is None:
            parser.error("the following arguments are required: args.  [name] not given")
        config = args.config if args.config else vctf.get_ctf_config(name)
        c = ctf.get_platform_object(config)
        c.list()

    # pull challenge files and create directories
    #   `pull [name]`
    elif command == 'pull' or command == 'p':
        name = get_name_or_active(args)
        if args.args is None:
            parser.error("the following arguments are required: args.  [name] not given")
        config = args.config if args.config else vctf.get_ctf_config(name)
        c = ctf.get_platform_object(config)
        c.pull()

    # submit a given flag for given challenge_id
    #   `submit id flag`
    elif command == 'submit':
        try:
            name = vctf.get_active()
        except FileNotFoundError:
            parser.error("must be in an active CTF")
        if args.args is None or len(args.args) < 2:
            parser.error("the following arguments are required: args.  [challenge_id flag] not given")
        id = args.args[0]
        flag = args.args[1]
        config = args.config if args.config else vctf.get_ctf_config(name)
        c = ctf.get_platform_object(config)
        c.submit(id, flag)

    else:
        parser.error("command not supported")

if __name__ == '__main__':
    main()
