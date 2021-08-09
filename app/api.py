from json import loads
from urllib import parse
from urllib.request import Request
from urllib.request import urlopen

from flask import request
from flask import current_app


def get_json(url: str, payload: dict):
    # `payload` 파싱
    payload = parse.urlencode(query=payload)

    req = Request(
        url=f"{url}?{payload}",
        method="GET",
        headers={
            "User-Agent": f"SchoolMeal (https://github.com/chick0/meal; {request.host})"
        }
    )

    # 요청 전송하기
    resp = urlopen(req, timeout=5)
    return loads(resp.read())


def search_school_by_name(school_name: str):
    return get_json(
        url="https://open.neis.go.kr/hub/schoolInfo",
        payload={
            "key": current_app.config['API_KEY'],
            "type": "json",
            "pIndex": 1,
            "pSize": 30,

            "SCHUL_NM": school_name
        }
    )


def search_meal_by_codes(edu_code: str, school_code: str, date: str):
    return get_json(
        url="https://open.neis.go.kr/hub/mealServiceDietInfo",
        payload={
            "key": current_app.config['API_KEY'],
            "type": "json",
            "pIndex": 1,

            "ATPT_OFCDC_SC_CODE": edu_code,
            "SD_SCHUL_CODE": school_code,
            "MLSV_YMD": date
        }
    )
