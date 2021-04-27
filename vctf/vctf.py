import configparser
import os
import shutil
import subprocess

from vctf.ctf import platforms, default_platform_name


TEMPLATE_DIR = '.template'
MISC_DIR = '.misc'
CONFIG_DIR = '.config'
ACTIVE_CTF = '.active_ctf'

TEMPLATE_NAME = 'solve.py'
DEFAULT_TEMPLATE = b"""# run `pwn template > solve.py`
# This is the default template at $PROJECT_HOME/.template/solve.py
"""

FAKE_FLAG = b'FLAG{THIS_IS_A_FLAG}'
FLAG_FILES = ['flag', 'flag.txt']

def get_project_home():
    return os.getenv('PROJECT_HOME')

def get_config_directory():
    project_home = get_project_home()
    config_directory = os.path.join(project_home, CONFIG_DIR)
    if not os.path.exists(config_directory):
        os.mkdir(config_directory)
    return config_directory

def get_ctf_config(name):
    config_directory = get_config_directory()
    ctf_config = os.path.join(config_directory, name + '.ini')
    if not os.path.exists(ctf_config):
        with open(ctf_config, 'w') as f:
            f.write('')
    return ctf_config

def get_active():
    project_home = get_project_home()
    active_ctf = os.path.join(project_home, ACTIVE_CTF)
    with open(active_ctf, 'r') as f:
        name = f.read()
    return name

def set_active(name):
    ## Set as active CTF
    project_home = get_project_home()
    active_ctf = os.path.join(project_home, ACTIVE_CTF)
    with open(active_ctf, 'w') as f:
        f.write(name)

    ## Setup virtualenv
    subprocess.check_call(['startctf', name])

def init(config, name, username=None, password=None, url=None, platform=None, directory=None, project_home=None):
    """
    Initialize a CTF, saves config, and sets it as the active
    """
    if platform != None:
        for key in platforms:
            if platform.lower() == key.lower():
                platform = key
                break
        else:
            raise Exception("Given platform is not supported")

    # set CTFs' root directory
    if project_home == None:
        project_home = get_project_home()

    # set CTF root directory
    if directory:
        ctf_directory = directory
    else:
        ctf_directory = os.path.join(project_home, name)
    if not os.path.exists(ctf_directory):
        os.mkdir(ctf_directory)

    ## Create files in CTFs' root if not exist
    # create misc directory if not exist
    # - misc files are used to copy over files used for every, non-unique to a CTF
    misc_dir = os.path.join(project_home, MISC_DIR)
    if not os.path.exists(misc_dir):
        os.mkdir(misc_dir)

    # create template directory if not exist
    # - template files are solve.py, flag, and flag.txt, they can be unique per CTF
    template_dir = os.path.join(project_home, TEMPLATE_DIR)
    if not os.path.exists(template_dir):
        os.mkdir(template_dir)

    # create solve script if not exist
    template_script = os.path.join(template_dir, TEMPLATE_NAME)
    if not os.path.exists(template_script):
        with open(template_script, 'wb') as f:
            f.write(DEFAULT_TEMPLATE)

    # create fake flag files if not exist
    for fname in FLAG_FILES:
        fpath = os.path.join(template_dir, fname)
        if not os.path.exists(fpath):
            with open(fpath, 'wb') as f:
                f.write(FAKE_FLAG)

    ## Save specific CTF template files
    # copy template directory into new CTF root
    for fname in os.listdir(template_dir):
        src_path = os.path.join(template_dir, fname)
        dst_path = os.path.join(ctf_directory, fname)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)


    ## Setup CTF config file
    config_parser = configparser.ConfigParser()

    # set ctf name
    config_parser['DEFAULT']['name'] = name

    # set creds
    config_parser['DEFAULT']['username'] = '' if username == None else username
    config_parser['DEFAULT']['password'] = '' if password == None else password

    # set platform
    config_parser['DEFAULT']['platform'] = default_platform_name if platform == None else platform

    # set url domain
    config_parser['DEFAULT']['url'] = '' if  url == None else url

    # set directories and save
    config_parser['DEFAULT']['directory'] = ctf_directory
    config_parser['DEFAULT']['project_home'] = project_home
    with open(config, 'w') as f:
        config_parser.write(f)

    ## Set as active CTF and setup virtualenv
    set_active(name)

def end():
    """
    Remove active CTF by removing .active_ctf file
    """
    project_home = get_project_home()
    active_ctf = os.path.join(project_home, ACTIVE_CTF)
    if os.path.isfile(active_ctf):
        os.remove(active_ctf)

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
    ctf_name = get_active()
    ctf_directory = os.path.join(project_home, ctf_name)

    # create category if not exist
    category_path = os.path.join(ctf_directory, category)
    if not os.path.exists(category_path):
        os.mkdir(category_path)

    # create challenge directory
    challenge_path = os.path.join(category_path, name)
    if not os.path.exists(challenge_path):
        os.mkdir(challenge_path)
    else:
        # already populated, skip and return
        return challenge_path

    # populate challenge directory
    files = get_challenge_files(project_home, ctf_directory)
    for src_path in files:
        dst_path = os.path.join(challenge_path, os.path.basename(src_path))
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
    return challenge_path
