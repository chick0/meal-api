# -*- coding: utf-8 -*-
from sys import exit

from conf import conf

# # # # # # # # # # # # # # # # # # # # # #

# DB 접속 정보 & 설정
try:
    SQLALCHEMY_DATABASE_URI = f"mysql://{conf['account']['user']}:{conf['account']['password']}" \
                              f"@{conf['database']['host']}/{conf['database']['database']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
except KeyError:
    print("오류: 데이터베이스 접속 정보를 불러오지 못함")
    exit(-1)

# # # # # # # # # # # # # # # # # # # # # #

# 세션 용 시크릿 키
try:
    SECRET_KEY = open(".SECRET_KEY", mode="rb").read()
except FileNotFoundError:
    SECRET_KEY = getattr(__import__("SECRET_KEY"), "SECRET_KEY")

# 세션 쿠키 설정
SESSION_COOKIE_NAME = "s"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Strict"

# # # # # # # # # # # # # # # # # # # # # #
