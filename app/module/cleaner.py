# -*- coding: utf-8 -*-
from json import loads, dumps


def clean(json_str: str):
    json = loads(json_str)

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

    return dumps(obj=json)
