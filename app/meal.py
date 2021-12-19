from re import findall
from json import dumps
from json import loads
from urllib.error import HTTPError

from redis.exceptions import ConnectionError

from app import redis
from app import no_redis
from .api import search_meal_by_codes


def reformat(json: list):
    table = {
        1: "난류",
        2: "우유",
        3: "메밀",
        4: "땅콩",
        5: "대두",
        6: "밀",
        7: "고등어",
        8: "게",
        9: "새우",
        10: "돼지고기",
        11: "복숭아",
        12: "토마토",
        13: "아황산류",
        14: "호두",
        15: "닭고기",
        16: "쇠고기",
        17: "오징어",
        18: "조개류",
        19: "잣",
    }

    new_json = []

    for item in json:
        menu_list = []
        for menu in item['DDISH_NM'].split("<br/>"):
            code = [int(code) for code in "".join(findall(r"[0-9.]", menu)).split(".") if len(code) != 0]
            code = sorted(code, reverse=True)

            for cd in code:
                menu = menu.replace(str(cd), "")

            try:
                menu_list.append({
                    "name": menu.replace(".", ""),
                    "allergy": [table[key] for key in sorted(code)]
                })
            except KeyError:
                menu_list.append({
                    "name": menu,
                    "allergy": []
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


def get_meal_data_by_codes(edu: str, school: str, date: str):
    def fetch_from_redis() -> list or None:
        if no_redis:
            return None

        try:
            return loads(
                redis.get(
                    name=f"{edu}#{school}#{date}"
                )
            )
        except (ConnectionError, TypeError, Exception):
            return None

    def add_cache(json: list):
        try:
            redis.set(
                name=f"{edu}#{school}#{date}",
                value=dumps(json), ex=604800
            )
        except ConnectionError:
            pass

    result = fetch_from_redis()

    if result is None:
        def fetch_from_api() -> dict or bool or None:
            try:
                return search_meal_by_codes(
                    edu_code=edu,
                    school_code=school,
                    date=date
                )
            except (HTTPError, Exception):
                return False

        result = fetch_from_api()
        if isinstance(result, dict):
            try:
                result = [j['row'] for j in [i for i in result['mealServiceDietInfo']] if "row" in j][0]
            except KeyError:
                result = []

            if result:
                result = reformat(json=result)

            if not no_redis:
                add_cache(json=result)

    return result
