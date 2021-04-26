import configparser
import json
import os
import re
import string

import pandas
import requests
from urllib.parse import urlparse


# for parsing challenge names, characteres chosen for personal preferance
parsed_challenge_alphabet = string.ascii_letters + string.digits  + '-_'


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
        pass
    def list(self):
        """
        list challenges
        """
        pass
    def add(self):
        """
        manually add challenge
        """
        pass
    def delete(self):
        """
        manually delete challenge
        """
        pass
    def submit(self, id, flag):
        """
        submit a flag for a challenge
        """
        pass

class CTFd(CTF):
    def __init__(self, config_filename):
        super().__init__(config_filename)
        self._auth()

    def _auth(self):
        """
        Sets session using username/password
        """
        self.session = requests.session()

        # get nonces/tokens
        r = self.session.get(self.url + '/login')
        if not r.ok:
            raise Exception("Error querying site")

        # get nonce
        regex = re.compile('<input id="nonce" name="nonce" type="hidden" value="(.+)">')
        found = regex.findall(r.text)
        if len(found) < 1:
            raise Exception("nonce not found")
        nonce = found[0]

        # get csrfNonce
        regex = re.compile("""'csrfNonce': "(.+)",""")
        found = regex.findall(r.text)
        if len(found) < 1:
            raise Exception("csrfNonce not found")
        self.csrfNonce = found[0]

        # login with creds to set cookie
        auth_args = {
            "name": self.username,
            "password": self.password,
            "nonce": nonce,
        }
        r = self.session.post(self.url + '/login', data=auth_args)
        if not r.ok:
            raise Exception("Error logging in")

    def _challenges(self):
        """
        Requests challenges from CTFd api
        """
        route = '/api/v1/challenges'
        r = self.session.get(self.url + route)
        if not r.ok:
            print(r)
            print(r.text)
            raise Exception("Error getting challenges")

        results = json.loads(r.text)
        challenges = results["data"]
        return challenges

    def _challenge(self, id):
        """
        Requests a challenge from CTFd api
        """
        route = '/api/v1/challenges/' + str(id)
        r = self.session.get(self.url + route)
        if not r.ok:
            print(r)
            print(r.text)
            raise Exception("Error getting challenges")

        results = json.loads(r.text)
        challenge = results["data"]
        return challenge

    def _attempt(self, id, flag):
        """
        Attempt a flag for a given challenge
        """
        # update csrf token
        route = '/challenges'
        r = self.session.get(self.url + route)
        if not r.ok:
            raise Exception("Error querying site")

        # get csrfNonce
        regex = re.compile("""'csrfNonce': "(.+)",""")
        found = regex.findall(r.text)
        if len(found) < 1:
            raise Exception("csrfNonce not found")
        self.csrfNonce = found[0]


        route = '/api/v1/challenges/attempt'
        data = {"challenge_id": int(id), "submission": flag}
        headers = {"CSRF-Token": self.csrfNonce}
        r = self.session.post(self.url + route, json=data, headers=headers)
        if not r.ok:
            raise Exception("Error getting challenges")

        results = json.loads(r.text)
        status = results["data"]
        return status

    def list(self):
        """
        Prints challenges to stdout
        """
        challenges = self._challenges()
        columns = ["id", "category", "name", "value", "solves", "solved_by_me"]
        df = pandas.DataFrame(challenges, columns=columns)
        print(df)

    def pull(self):
        """
        Gets challenges and makes appropriate directories locally
        """
        from vctf.vctf import add_challenge

        challenges = self._challenges()
        for c in challenges:
            id = c['id']
            challenge = self._challenge(id)

            name = challenge["name"]
            category = challenge["category"]
            files = challenge["files"]
            #view = challenge["view"]
            #value = challenge["value"]
            #description = challenge["description"]

            name = parse_challenge_name(name)
            category = parse_challenge_name(category)
            challenge_path = add_challenge(category, name)
            s = "Challenge: {cat} - {name} ({id}): {path}".format(cat=category, name=name, id=id, path=challenge_path)
            print(s)

            for route in files:
                r = urlparse(route)
                filename = os.path.basename(r.path)

                # quick check to determine if we escape up a directory
                challenge_file = os.path.join(challenge_path, filename)
                c = os.path.realpath(challenge_file)
                d = os.path.realpath(challenge_path)
                if d != os.path.commonpath((c,d)):
                    print("error adding file for challenge {id}".format(id=id))
                    continue
                if not os.path.exists(c):
                    url = self.url + route
                    r = self.session.get(url)
                    with open(c, 'wb') as f:
                        f.write(r.content)
                    print(" [+] Added file for challenge {id} '{filename}'".format(id=id, filename=c))

    def submit(self, id, flag):
        """
        Submits a flag for a challenge
        """
        status = self._attempt(id, flag)
        message = status['message']
        print(message)
        if status == 'incorrect':
            return False
        else:
            return True


platforms = {
    "CTFd": CTFd,
}

def get_plaforms():
    return [k for k in platforms]

def get_platform_object(config_filename):
    config_parser = configparser.ConfigParser()
    config_parser.read(config_filename)
    platform = config_parser['DEFAULT']['platform']
    ctf = platforms[platform]
    return ctf(config_filename)

def parse_challenge_name(name):
    parsed_name = ''
    for c in name:
        if c in parsed_challenge_alphabet:
            parsed_name += c
        else:
            parsed_name += '_'
    return parsed_name
