# -*- coding: utf-8 -*-
from os import path, mkdir
from sys import exit

from conf import conf


# DB 접속 정보 & 설정
try:
    SQLALCHEMY_DATABASE_URI = f"mysql://{conf['account']['user']}:{conf['account']['password']}" \
                              f"@{conf['database']['host']}/{conf['database']['database']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
except KeyError:
    print("데이터베이스 접속 정보를 불러오지 못함\n"
          "- 'conf/database.ini' 파일을 수정하세요")
    with open(path.join("conf", "database.ini"), mode="w") as fp:
        fp.write("[account]\n")
        fp.write("user=\n")
        fp.write("password=\n\n")
        fp.write("[database]\n")
        fp.write("host=\n")
        fp.write("database=")
    exit(-1)


# 세션 용 시크릿 키
try:
    SECRET_KEY = open(path.join("conf", "SECRET_KEY"), mode="rb").read()
except FileNotFoundError:
    print("'SECRET_KEY' 파일을 찾지 못함\n"
          "- 'SECRET_KEY.py' 스크립트를 실행하세요")
    exit(-2)


del path, mkdir, exit, conf
