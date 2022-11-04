from re import compile
from json import dumps
from json import loads
from urllib.error import HTTPError
from logging import getLogger

from flask import current_app as app
from redis.exceptions import ConnectionError

from app.api import search_meal_by_codes

logger = getLogger()


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

    re = compile(r"([0-9.]){2,}")

    for item in json:
        menu_list = []
        for menu in item['DDISH_NM'].split("<br/>"):
            search = re.search(menu)

            if search is None:
                display = menu
                allergy = []
                codes = []
            else:
                codes = menu[search.start():search.end()]
                display = menu.replace(codes, "")

                codes = [int(x) for x in codes.split(".") if len(x) != 0]

                allergy = []
                for code in codes:
                    # 알러지 식품명 표에서 가져오기
                    # 표에 등록된 식품이 아니라면 그냥 숫자 코드 등록하기
                    allergy.append(table.get(code, str(code)))

            display = display.replace("()", "").strip()

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
    def addr(sep: str = " ") -> str:
        return sep.join([edu, school, date])

    def fetch_from_redis() -> list or None:
        if app.redis is None:
            return None

        try:
            from_redis = app.redis.get(name=addr("#"))

            if from_redis is None:
                return None

            logger.info(f"Get meal date from redis / {addr()}")
            return loads(from_redis)
        except (ConnectionError, TypeError, Exception):
            logger.exception("Exception in getting data from redis")
            return None

    def add_cache(json: list):
        try:
            app.redis.set(
                name=addr("#"),
                value=dumps(json),
                ex=604800
            )

            logger.info(f"Add meal data to redis / {addr()}")
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
                logger.exception("Exception in meal data api request")
                return False

        logger.info(f"Get meal date from api / {addr()}")
        result = fetch_from_api()

        if isinstance(result, dict):
            try:
                result = [j['row'] for j in [i for i in result['mealServiceDietInfo']] if "row" in j][0]
            except KeyError:
                result = []

            if result:
                result = reformat(json=result)

            if app.redis is not None:
                add_cache(json=result)

    return result
