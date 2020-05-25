#!/usr/bin/env python
"""
Create CTF work directory with virtualenvwrapper
"""
import logging
import os
import subprocess

log = logging.getLogger(__name__)


def template(args):
    """
    """
    project_name = os.path.basename(os.getenv('VIRTUAL_ENV'))
    project_path = os.getenv('PROJECT_HOME')
    
    filepath = os.path.join(project_path, project_name)
    subprocess.check_call(['initctf.py', filepath])
