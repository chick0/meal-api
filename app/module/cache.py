# -*- coding: utf-8 -*-
from json import loads, dumps
from json import JSONDecodeError

from redis.exceptions import ConnectionError

from app import redis


def clean(json: list):
    allow_keys = [
        "SCHUL_NM",       # 학교 이름
        "MMEAL_SC_CODE",  # 식사 코드 (  1 /  2 /  3 )
        "MMEAL_SC_NM",    # 식사 명   (조식/중식/석식)
        "DDISH_NM",       # 메뉴
        "ORPLC_INFO",     # 원산지 정보
        "CAL_INFO",       # 칼로리
        "NTR_INFO"        # 영양정보
    ]

    for i in range(0, len(json)):
        for key in [key for key in json[i].keys() if key not in allow_keys]:
            del json[i][key]

    return json


# 교육청 코드와 학교 코드와 날짜 정보로 캐시 불러오는 함수
def get_cache_by_data(edu: str, school: str, date: str):
    try:
        return loads(
            redis.get(
                name=f"{edu}#{school}#{date}"
            )
        )
    except (ConnectionError, TypeError, JSONDecodeError):
        return None


# 캐시 저장하는 함수
def add_cache(edu: str, school: str, date: int, json: list):
    try:
        redis.set(
            name=f"{edu}#{school}#{date}",
            value=dumps(clean(json))
        )
    except ConnectionError:
        pass
