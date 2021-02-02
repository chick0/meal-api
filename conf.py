# -*- coding: utf-8 -*-
from os import path, mkdir, listdir
from configparser import ConfigParser

if not path.exists("conf"):
    mkdir("conf")

conf = ConfigParser()
for file in [f for f in listdir(path.join("conf")) if f.endswith(".ini")]:
    conf.read(path.join("conf", file), "utf-8")
