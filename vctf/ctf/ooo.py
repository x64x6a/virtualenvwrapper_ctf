import json
import os
import re

import pandas
import requests
from urllib.parse import urlparse

from vctf.ctf.ctf import CTF
from vctf.ctf.ctf import parse_challenge_name


# main categories that will take priority in order
categories = ["web", "pwn", "reversing"]
challenge_file_regex = re.compile(r"\]\((.+)\)")

class OOO(CTF):
    def __init__(self, config_filename):
        super().__init__(config_filename)
        self._auth()

    def _auth(self):
        """
        Sets session using username/password
        """
        self.session = requests.session()

    def _challenges(self):
        """
        Gets challenges
        """
        route = "/scoreboard.json"
        r = self.session.get(self.url + route)
        if not r.ok:
            print(r)
            print(r.text)
            raise Exception("Error getting challenges")

        json_challenges = json.loads(r.text)
        challenges = []
        for challenge_name in json_challenges:
            c = json_challenges[challenge_name]
            for cat in c["tags"]:
                if cat in categories:
                    category = cat
                    break
            else:
                category = c["tags"][0]
            description = c["description"]
            files = challenge_file_regex.findall(description)
            challenge = {
                "name": challenge_name,
                "category": category,
                "description": description,
                "files": files,
                "tags": c["tags"],
            }
            challenges.append(challenge)
        return challenges

    def list(self):
        """
        Prints challenges to stdout
        """
        challenges = self._challenges()
        columns = ["name", "category", "tags", "description"]
        df = pandas.DataFrame(challenges, columns=columns)
        print(df)

    def pull(self):
        """
        Gets challenges and makes appropriate directories locally
        """
        from vctf.vctf import add_challenge

        challenges = self._challenges()
        for challenge in challenges:
            name = challenge["name"]
            category = challenge["category"]
            files = challenge["files"]

            name = parse_challenge_name(name)
            category = parse_challenge_name(category)
            challenge_path = add_challenge(category, name)
            s = "Challenge: {cat} - {name}: {path}".format(cat=category, name=name, path=challenge_path)
            print(s)

            for route in files:
                r = urlparse(route)
                filename = os.path.basename(r.path)

                # quick check to determine if escape up a directory
                challenge_file = os.path.join(challenge_path, filename)
                c = os.path.realpath(challenge_file)
                d = os.path.realpath(challenge_path)
                if d != os.path.commonpath((c,d)):
                    print("error adding file for challenge \"{name}\"".format(name=name))
                    continue
                if not os.path.exists(c):
                    url = self.url + route
                    r = self.session.get(url)
                    with open(c, 'wb') as f:
                        f.write(r.content)
                    print(" [+] Added file for challenge \"{name}\" '{filename}'".format(name=name, filename=c))
