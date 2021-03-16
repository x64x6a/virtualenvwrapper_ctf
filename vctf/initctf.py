#!/usr/bin/env python
import os
import shutil


TEMPLATE_CTF = '.template'
MISC_DIR = '.misc'

TEMPLATE_NAME = 'solve.py'
DEFAULT_TEMPLATE = b"""# run `pwn template > solve.py`
# This is the default template at $PROJECT_HOME/.template/solve.py
"""

FAKE_FLAG = b'FLAG{THIS_IS_A_FLAG}'
FLAG_FILES = ['flag', 'flag.txt']


def initctf(name):
    """
    Copy files into CTF work directory

    name - Name of CTF directory within $PROJECT_HOME directory
    """
    project_home = os.getenv('PROJECT_HOME')
    ctf_directory = os.path.join(project_home, name)
    if not os.path.exists(ctf_directory):
        os.mkdir(ctf_directory)

    # create misc directory if not exist
    misc_dir = os.path.join(project_home, MISC_DIR)
    if not os.path.exists(misc_dir):
        os.mkdir(misc_dir)

    # create template ctf if not exist
    template_ctf_directory = os.path.join(project_home, TEMPLATE_CTF)
    if not os.path.exists(template_ctf_directory):
        os.mkdir(template_ctf_directory)

    # create base template script if not exist
    template_script = os.path.join(template_ctf_directory, TEMPLATE_NAME)
    if not os.path.exists(template_script):
        with open(template_script, 'wb') as f:
            f.write(DEFAULT_TEMPLATE)

    # create fake flag files if not exist
    for fname in FLAG_FILES:
        fpath = os.path.join(template_ctf_directory, fname)
        if not os.path.exists(fpath):
            with open(fpath, 'wb') as f:
                f.write(FAKE_FLAG)

    # copy template directory into new CTF
    for fname in os.listdir(template_ctf_directory):
        src_path = os.path.join(template_ctf_directory, fname)
        dst_path = os.path.join(ctf_directory, fname)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
