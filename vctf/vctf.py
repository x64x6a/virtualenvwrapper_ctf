import configparser
import os
import shutil
import subprocess

from vctf.ctf import CTFd


platforms = {
    "CTFd": CTFd,
}

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
    if platform != None and plaform not in plaforms:
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
    config_parser['DEFAULT']['name'] = name
    if username != None:
        config_parser['DEFAULT']['username'] = username
    if password != None:
        config_parser['DEFAULT']['password'] = password
    if platform != None:
        config_parser['DEFAULT']['platform'] = platform
    if url != None:
        config_parser['DEFAULT']['url'] = url
    config_parser['DEFAULT']['directory'] = ctf_directory
    config_parser['DEFAULT']['project_home'] = project_home
    with open(config, 'w') as f:
        config_parser.write(f)

    ## Set as active CTF and setup virtualenv
    set_active(name)

def load(config):
    """
    Loads a CTF from config and sets as active
    """
    pass

def end(config):
    """
    Remove current CTF as active
    """
    pass


def pull(config):
    """
    Pull challenges for active CTF
    """
    pass

def add(config, challenge):
    """
    Manually add challenge for active CTF
    """
    pass

def delete(config, challenge):
    """
    Manually delete challenge for active CTF
    """
    pass

def submit(config, challenge, flag):
    """
    Submit a given flag for a given challenge for the active CTF
    """
    pass