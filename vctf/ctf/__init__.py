import configparser
from vctf.ctf.ctf import CTF
from vctf.ctf.ctfd import CTFd
from vctf.ctf.ooo import OOO


platforms = {
    "CTF": CTF,
    "CTFd": CTFd,
    "OOO": OOO,
}

default_platform = CTF
default_platform_name = 'CTF'

def get_platforms():
    return [k for k in platforms]

def get_platform_object(config_filename):
    config_parser = configparser.ConfigParser()
    config_parser.read(config_filename)
    platform = config_parser['DEFAULT']['platform']
    if platform == default_platform_name:
        return default_platform(config_filename)
    elif platform in platforms:
        ctf = platforms[platform]
        return ctf(config_filename)
    else:
        err = "{} not in platforms".format(platform)
        raise Exception(err)
