# -*- coding: utf-8 -*-
from json import loads
from urllib import parse
from urllib.request import Request, urlopen

from conf import conf


def get_json(url: str, payload: dict):
    # `payload` 파싱
    payload = parse.urlencode(query=payload)

    req = Request(
        url=f"{url}?{payload}",
        method="GET",
        headers={
            "User-Agent": f"MealWeb (https://github.com/chick0/meal; {conf['app']['host']})"
        }
    )

    # 요청 전송하기
    resp = urlopen(req, timeout=5)
    return loads(resp.read())


def search_school_by_name(school_name: str):
    target_url = "https://open.neis.go.kr/hub/schoolInfo"

    payload = dict()

    payload['key'] = conf['api']['n']
    payload['type'] = "json"
    payload['pIndex'] = 1
    payload['pSize'] = 30

    payload['SCHUL_NM'] = school_name

    return get_json(
        url=target_url,
        payload=payload
    )


def search_meal_by_codes(edu_code: str, school_code: str, date: str):
    target_url = "https://open.neis.go.kr/hub/mealServiceDietInfo"

    payload = dict()

    payload['key'] = conf['api']['n']
    payload['type'] = "json"
    payload['pIndex'] = 1

    payload['ATPT_OFCDC_SC_CODE'] = edu_code
    payload['SD_SCHUL_CODE'] = school_code

    payload['MLSV_YMD'] = date

    return get_json(
        url=target_url,
        payload=payload
    )
