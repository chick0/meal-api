# -*- coding: utf-8 -*-
from json import dumps
from datetime import datetime
from urllib.error import HTTPError

from flask import Blueprint
from flask import request
from flask import Response

from app import redis
from app.module.cache import get_cache_by_data, add_cache
from app.module.api import search_meal_by_codes
from app.module.search import query_filter
from app.module.search import get_school_data_by_query


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
    a, b = redis.srandmember("api:read", 1)[0].decode().split("::")
    return Response(
        status=200,
        mimetype="application/json",
        response=dump_to_return({"a": a, "b": b})
    )


# # # # # # # # # # # # # # # # # # # #


@bp.route("/school")
def school():
    def error(msg: str):
        return Response(
            status=400,
            mimetype="application/json",
            response=dump_to_return(dict(
                message=msg
            ))
        )

    # 학교 이름 가져오고 검색어 필터링
    status, school_name = query_filter(school_name=request.args.get("school_name", ""))

    # 검색어가 필터링된 경우
    if not status:
        return error(msg="해당 검색어는 사용이 불가능 합니다")

    # 학교 검색 결과 불러오기
    result = get_school_data_by_query(query=school_name)

    if result is None:
        # API 서버에서 받은 정보가 없으면
        return error(msg="검색 결과가 없습니다")
    elif result is False:
        # 교육청 점검 or 타임아웃
        return error(msg="학교 목록을 불러오는 데 실패했습니다")

    # 검색 결과가 있으면 학교 목록 리턴
    return Response(
        status=200,
        mimetype="application/json",
        response=dump_to_return(json=result)
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
