# -*- coding: utf-8 -*-
from re import findall
from json import loads, dumps
from json import JSONDecodeError

from redis.exceptions import ConnectionError

from app import redis


def reformat(json: list):
    table = {
        1: "달걀",     10: "돼지고기",
        2: "복숭아",   11: "우유",
        3: "메밀",     12: "토마토",
        4: "아황산염", 13: "땅콩",
        5: "대두",     14: "호두",
        6: "닭고기",   15: "밀",
        7: "고등어",   16: "쇠고기",
        8: "오징어",   17: "게",
        9: "새우",     18: "조개"
    }

    new_json = []

    for item in json:
        menu_list = []
        for menu in item['DDISH_NM'].split("<br/>"):
            code = [int(code) for code in "".join(findall(r"[0-9.]", menu)).split(".") if len(code) != 0]
            code = sorted(code, reverse=True)

            for cd in code:
                menu = menu.replace(str(cd), "")

            menu_list.append({
                "name": menu.replace(".", ""),
                "allergy": [table[key] for key in sorted(code)]
            })

        new_json.append({
            "school": item['SCHUL_NM'],
            "code": [item['MMEAL_SC_CODE'], item['MMEAL_SC_NM']],

            "calorie": item['CAL_INFO'],
            "nutrient": item['NTR_INFO'].split("<br/>"),
            "origin": item['ORPLC_INFO'].split("<br/>"),

            "menu": menu_list
        })

    return new_json


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
def add_cache(edu: str, school: str, date: str, json: list):
    json = reformat(json)

    try:
        redis.set(
            name=f"{edu}#{school}#{date}",
            value=dumps(json, ensure_ascii=False)
        )
    except ConnectionError:
        pass

    return json
