# -*- coding: utf-8 -*-
from os import path, mkdir, listdir
from configparser import ConfigParser

if not path.exists("conf"):
    mkdir("conf")

conf = ConfigParser()
for conf_file in listdir(path.join("conf")):
    if conf_file.endswith(".ini"):
        conf.read(path.join("conf", conf_file), "utf-8")
