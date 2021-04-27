import configparser
import string


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
        from vctf.vctf import add_challenge
        return add_challenge(category, name)
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
