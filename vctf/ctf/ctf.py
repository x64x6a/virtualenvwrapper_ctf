import configparser
import os
import shutil
import string


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


class CTF(object):
    def __init__(self, config_filename):
        config_parser = configparser.ConfigParser()
        config_parser.read(config_filename)

        #  this will key error if fields do not exist
        self.name = config_parser['DEFAULT']['name']
        self.username = config_parser['DEFAULT']['username']
        self.password = config_parser['DEFAULT']['password']
        self.platform = config_parser['DEFAULT']['platform']
        self.url = config_parser['DEFAULT']['url']
        self.directory = config_parser['DEFAULT']['directory']
        self.project_home = config_parser['DEFAULT']['project_home']
    def pull(self):
        """
        pull challenges
        """
        print("pull not supported for {}".format(self.platform))
    def list(self):
        """
        list challenges
        """
        print("list not supported for {}".format(self.platform))
    def add(self, category, name):
        """
        manually add challenge
        """
        project_home = self.project_home
        ctf_name = self.name
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

    def delete(self, *args):
        """
        manually delete challenge
        """
        print("delete not supported for {}".format(self.platform))
    def submit(self, *args):
        """
        submit a flag for a challenge
        """
        print("submit not supported for {}".format(self.platform))


# for parsing challenge names, characteres chosen for personal preferance
parsed_challenge_alphabet = string.ascii_letters + string.digits  + '-_'

def parse_challenge_name(name):
    parsed_name = ''
    for c in name:
        if c in parsed_challenge_alphabet:
            parsed_name += c
        else:
            parsed_name += '_'
    return parsed_name
