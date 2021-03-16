#!/usr/bin/env python
import argparse
import os
import shutil


MISC_DIR = '.misc'
TEMPLATE_NAME = 'solve.py'
FLAG_FILES = ['flag', 'flag.txt']

def get_challenge_files(project_home, ctf_directory):
    """
    returns a list of files to copy into a challenge
    """
    files = []

    # copy debuggers and other misc files
    misc_dir = os.path.join(project_home, MISC_DIR)
    for fname in os.listdir(misc_dir):
        fpath = os.path.join(misc_dir, fname)
        files.append(fpath)

    # copy template script
    fpath = os.path.join(ctf_directory, TEMPLATE_NAME)
    files.append(fpath)

    # copy flags
    for fname in FLAG_FILES:
        fpath = os.path.join(ctf_directory, fname)
        files.append(fpath)

    return files


def add_challenge(category, name):
    project_home = os.getenv('PROJECT_HOME')
    virtual_env = os.getenv('VIRTUAL_ENV')
    ctf_name = os.path.basename(os.path.normpath(virtual_env))
    ctf_directory = os.path.join(project_home, ctf_name)

    # create category if not exist
    category_path = os.path.join(ctf_directory, category)
    if not os.path.exists(category_path):
        os.mkdir(category_path)

    # create challenge directory
    challenge_path = os.path.join(category_path, name)
    if not os.path.exists(challenge_path):
        os.mkdir(challenge_path)

    # populate challenge directory
    files = get_challenge_files(project_home, ctf_directory)
    for src_path in files:
        dst_path = os.path.join(challenge_path, os.path.basename(src_path))
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
