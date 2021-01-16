# -*- coding: utf-8 -*-
from json import loads
from urllib import request, parse

from conf import conf


def get_json(url: str, payload: dict):
    # `payload` 파싱
    payload = parse.urlencode(query=payload)

    # `URL`에 `payload` 합쳐서 `full_url` 만들기
    full_url = f"{url}?{payload}"

    # `full_url`에 요청하기
    with request.urlopen(url=full_url) as resp:
        if resp.status == 200:  # 웹 서버 응답이 200인 경우
            # 헤더 값에서 응답을 `json`이 아니라 `html`로 주기에
            # json 모듈을 통해 딕셔너리로 전환
            return loads(resp.read()), 200
        else:  # 아닌 경우
            return False, resp.status


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
