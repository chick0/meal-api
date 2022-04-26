from json import dumps
from json import loads
from urllib.error import HTTPError

from flask import current_app
from redis.exceptions import ConnectionError

from app import redis
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
            display, codes = menu.split("  ")

            codes = [int(x)
                     # 괄호 제거 & . 을 기준으로 자르기
                     for x in codes.replace("(", "").replace(")", "").split(".") if len(x) != 0]

            allergy = []
            for code in codes:
                # 알러지 식품명 표에서 가져오기
                # 표에 등록된 식품이 아니라면 그냥 숫자 코드 등록하기
                allergy.append(table.get(code, str(code)))

            menu_list.append({
                "name": display,
                "allergy": allergy,
                "allergy_code": codes
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
        if current_app.config.get("NO_REDIS"):
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

            if not current_app.config.get("NO_REDIS"):
                add_cache(json=result)

    return result
