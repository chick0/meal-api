#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import urandom, stat
from os import path, mkdir, rename
from datetime import datetime
from logging import getLogger
from logging import FileHandler

from waitress import serve
from paste.translogger import TransLogger

from app import create_app
from conf import conf


if __name__ == "__main__":
    # 기존 서버 로그가 있다면
    if path.exists("wsgi.log"):
        # 기존 로그 보관 풀더가 있는지 검사, 없으면 만들기
        if not path.exists("log archive"):
            mkdir("log archive")

        # 기존 로그의 사이즈가 0이 아니라면 보관 풀더로 이동
        if stat("wsgi.log").st_size != 0:
            # 기존 로그의 생성 날짜 가져오기
            last = datetime.fromtimestamp(path.getctime("wsgi.log"))

            def archive():
                # 중복방지를 위한 랜덤 코드 만들기
                code = urandom(4).hex()

                try:
                    # 만든 랜덤코드와 기존 로그의 생성 날짜를 이용해 보관 풀더로 이동
                    rename(
                        "wsgi.log",
                        path.join("log archive", last.strftime(f"%Y-%m-%d %Hh %Mm %Ss {code}.log"))
                    )
                except FileExistsError:
                    # 랜덤코드가 겹치면 다시 시도하기
                    archive()

            # 기존 로그파일 보관하는 함수 실행하기
            archive()

    # 로거 핸들러 가져오기, 파일 핸들러 등록하기
    logger = getLogger("wsgi")
    logger.addHandler(FileHandler("wsgi.log"))

    # `conf/server.ini`에 설정된 포트로 웹 서버 시작
    serve(
        app=TransLogger(
            application=create_app()
        ),
        port=conf['server']['port'],
    )
