# -*- coding: utf-8 -*-

from redis.exceptions import ConnectionError

from app import redis
from app.module.cleaner import clean


# 교육청 코드와 학교 코드와 날짜 정보로 캐시 불러오는 함수
def get_cache_by_data(edu: str, school: str, date: str):
    name = f"{edu}#{school}#{date}"

    try:
        json = redis.get(name)
    except ConnectionError:
        json = None

    return json


# 캐시 저장하는 함수
def add_cache(edu: str, school: str, date: int, json: str):
    name = f"{edu}#{school}#{date}"
    json = clean(json_str=json)

    try:
        redis.set(name, json)
    except ConnectionError:
        pass
