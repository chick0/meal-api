# -*- coding: utf-8 -*-
from re import findall
from json import loads, dumps
from random import choice
from datetime import datetime
from urllib.error import HTTPError

from flask import Blueprint
from flask import request
from flask import Response

from app import redis
from app.module.cache import get_cache_by_data, add_cache
from app.module.api import search_school_by_name, search_meal_by_codes


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


def dump_to_return(json: dict or list):
    return dumps(
        json, ensure_ascii=False
    )


@bp.route("/read")
def read():
    ctx = loads(redis.get(choice(redis.keys("api_read_*"))))
    return Response(
        status=200,
        mimetype="application/json",
        response=dump_to_return(dict(
            a=ctx.get("a"), b=ctx.get("b")
        ))
    )


# # # # # # # # # # # # # # # # # # # #


@bp.route("/school")
def school():
    # 요청에서 학교 이름 가져오기
    school_name = request.args.get("name", "")
    school_name = "".join(findall("[가-힣]", school_name))

    # 검색어가 없는 경우
    if school_name is None or len(school_name) == 0:
        return Response(
            status=400,
            mimetype="application/json",
            response=dump_to_return(dict(
                message="검색어를 입력해주세요"
            ))
        )

    # 금지된 검색어들
    if school_name in ["초등", "초등학교", "중", "중학교", "고등", "고등학교", "학교"]:
        return Response(
            status=400,
            mimetype="application/json",
            response=dump_to_return(dict(
                message="해당 검색어는 사용이 불가능 합니다"
            ))
        )

    try:
        # 검색어로 학교 찾기
        result = search_school_by_name(
            school_name=school_name
        )
    except HTTPError:
        # 교육청 점검 or 타임아웃
        return Response(
            status=400,
            mimetype="application/json",
            response=dump_to_return(dict(
                message="학교 목록을 불러오는 데 실패했습니다"
            ))
        )

    try:
        # 학교 목록
        school_list = [
            {
                "name": f"({school_['LCTN_SC_NM']}) {school_['SCHUL_NM']}",
                "edu": school_['ATPT_OFCDC_SC_CODE'],
                "school": school_['SD_SCHUL_CODE']
            } for school_ in result['schoolInfo'][1]['row']
        ]

        # 검색 결과가 있으면 학교 목록 리턴
        return Response(
            status=200,
            mimetype="application/json",
            response=dump_to_return(school_list)
        )
    except (KeyError, Exception):
        # API 서버에서 받은 정보에 학교 정보가 없으면
        return Response(
            status=404,
            mimetype="application/json",
            response=dump_to_return(dict(
                message="검색 결과가 없습니다"
            ))
        )


@bp.route("/meal")
def meal():
    edu_code = request.args.get("edu", None)
    school_code = request.args.get("school", None)
    date = request.args.get("date", datetime.now().strftime("%Y%m%d"))

    if edu_code is None or school_code is None:
        return Response(
            status=400,
            mimetype="application/json",
            response=dump_to_return(dict(
                message="교육청 코드와 학교 코드를 전달받지 못했습니다"
            ))
        )

    # Redis 에 저장된 캐시 검색
    result = get_cache_by_data(
        edu=edu_code,
        school=school_code,
        date=date
    )

    # 발견된 캐시 없음
    if result is None:
        try:
            # 교육청 서버에서 가져오기
            result = search_meal_by_codes(
                edu_code=edu_code,
                school_code=school_code,
                date=date
            )

            # 데이터 분해하기
            result = result['mealServiceDietInfo']

            # `row` 찾기
            for i in result:
                for j in i.keys():
                    if j == "row":
                        result = i[j]
                        break
        except KeyError:
            # 급식 없는 날 / 주말 또는 휴교일
            result = []
        except HTTPError:
            # 교육청 점검 or 타임아웃
            return Response(
                status=400,
                mimetype="application/json",
                response=dump_to_return(dict(
                    message="급식 정보를 불러오는 데 실패했습니다"
                ))
            )

        # Redis 에 급식 정보 캐싱
        result = add_cache(
            edu=edu_code,
            school=school_code,
            date=date,
            json=result
        )

    # 급식 출력하기
    return Response(
        status=200,
        mimetype="application/json",
        response=dump_to_return(result)
    )
