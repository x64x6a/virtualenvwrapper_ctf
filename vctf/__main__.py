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
    parser.add_argument('--directory', help='Specify CTF directory')
    parser.add_argument('--project_home', help='Specify directory if $PROJECT_HOME not used')

    args = parser.parse_args()
    command = args.command

    #init(config, name, username=None, password=None, url=None, platform=None, directory=None, project_home=None)
    if command == 'init' or command == 'i':
        if args.args is None or len(args.args) == 0:
            parser.error("the following arguments are required: args.  [name] not given")
        name = args.args[0]
        init_kwargs = {
            "username": args.username, "password": args.password,
            "url": args.url, "platform": args.platform,
            "directory": args.directory, "project_home": args.project_home
        }
        config = vctf.get_ctf_config(name)
        vctf.init(config, name, **init_kwargs)
    elif command == 'start' or command == 's':
        if args.args is None or len(args.args) == 0:
            parser.error("the following arguments are required: args.  [name] not given")
        name = args.args[0]
        vctf.set_active(name)
    elif command == 'end' or command == 'e':
        vctf.end()
    elif command == 'add' or command == 'a':
        if args.args is None or len(args.args) < 2:
            parser.error("the following arguments are required: args.  [category challenge] not given")
        category = args.args[0]
        challenge = args.args[1]
        vctf.add_challenge(category, challenge)
    elif command == 'list' or command == 'l':
        if args.args is None or len(args.args) == 0:
            try:
                name = vctf.get_active()
            except FileNotFoundError:
                name = None
            if name is None or len(name) == 0:
                parser.error("the following arguments are required: args.  [name] not given")
        else:
            name = args.args[0]
        config = vctf.get_ctf_config(name)
        c = ctf.get_platform_object(config)
        c.list()
    elif command == 'pull' or command == 'p':
        if args.args is None or len(args.args) == 0:
            try:
                name = vctf.get_active()
            except FileNotFoundError:
                name = None
            if name is None or len(name) == 0:
                parser.error("the following arguments are required: args.  [name] not given")
        else:
            name = args.args[0]
        config = vctf.get_ctf_config(name)
        c = ctf.get_platform_object(config)
        c.pull()
    elif command == 'submit':
        try:
            name = vctf.get_active()
        except FileNotFoundError:
            parser.error("must be in an active CTF")
        if args.args is None or len(args.args) < 2:
            parser.error("the following arguments are required: args.  [challenge_id flag] not given")
        id = args.args[0]
        flag = args.args[1]
        config = vctf.get_ctf_config(name)
        c = ctf.get_platform_object(config)
        c.submit(id, flag)
    else:
        parser.error("command not supported")

if __name__ == '__main__':
    main()
