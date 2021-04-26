import configparser
from vctf.ctf.ctfd import CTFd
from vctf.ctf.ooo import OOO


platforms = {
    "CTFd": CTFd,
    "OOO": OOO,
}

def get_platforms():
    return [k for k in platforms]

def get_platform_object(config_filename):
    config_parser = configparser.ConfigParser()
    config_parser.read(config_filename)
    platform = config_parser['DEFAULT']['platform']
    ctf = platforms[platform]
    return ctf(config_filename)
