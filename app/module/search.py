# -*- coding: utf-8 -*-
from re import findall
from json import loads, dumps
from json import JSONDecodeError
from hashlib import sha1
from urllib.error import HTTPError

from flask import url_for
from redis.exceptions import ConnectionError

from app import redis
from app.module.api import search_school_by_name


# 검색어 필터링
def query_filter(school_name: str):
    # 한글 완성자만 남기기
    school_name = "".join(findall("[가-힣]", school_name))

    # 검색어가 금지어인 경우 확인
    status = True if school_name not in ["초등", "초등학교", "중", "중학교", "고등", "고등학교", "학교"] else False

    if status:
        # 검색어가 0글자 이하인지 확인
        status = True if len(school_name) != 0 else False

    return status, school_name


# 검색 기록 불러오기
def get_school_data_by_query(query: str) -> list:
    def fetch_from_redis() -> list or None:
        try:
            return loads(
                redis.get(
                    name=f"search:{sha1(query.encode()).hexdigest()}"
                )
            )
        except (ConnectionError, TypeError, JSONDecodeError):
            return None

    # 캐시 저장하는 함수
    def add_cache(json: list):
        try:
            redis.set(
                name=f"search:{sha1(query.encode()).hexdigest()}",
                value=dumps(json), ex=86400
            )
        except ConnectionError:
            pass

    result = fetch_from_redis()

    if result is None:
        def fetch_from_api() -> dict or list or bool or None:
            try:
                return search_school_by_name(
                    school_name=query
                )
            except (HTTPError, Exception):
                return False

        result = fetch_from_api()
        if isinstance(result, dict):
            try:
                result = [
                    {
                        "name": f"({school['LCTN_SC_NM']}) {school['SCHUL_NM']}",
                        "url": url_for(
                            "meal.show",
                            edu_code=school['ATPT_OFCDC_SC_CODE'],
                            school_code=school['SD_SCHUL_CODE']
                        )
                    } for school in result['schoolInfo'][1]['row']
                ]

                add_cache(json=result)
            except (KeyError, Exception):
                result = None

    return result
