from datetime import datetime

from flask import Blueprint
from flask import request
from flask import jsonify

from app.search import query_filter
from app.search import get_school_data_by_query
from app.meal import get_meal_data_by_codes

bp = Blueprint(
    name="api",
    import_name="api",
    url_prefix="/api"
)


def error(code: str):
    errors = {
        "school": {
            "query_filtered": "해당 검색어는 사용이 불가능 합니다",
            "result_none": "검색 결과가 없습니다",
            "api_timeout_or_dead": "학교 목록을 불러오는 데 실패했습니다",
        },
        "meal": {
            "query_none": "교육청 코드와 학교 코드를 전달받지 못했습니다",
            "result_none": "급식 정보가 없습니다",
            "api_timeout_or_dead": "급식 정보를 불러오는 데 실패했습니다",
        },
    }

    tp, cd = code.split(".")
    message = errors.get(tp, {}).get(cd, "등록되지 않은 오류입니다. 개발자한테 신고해주세요.")

    return jsonify({
        "code": code,
        "message": message
    }), 400


@bp.get("/school")
def school():
    # 학교 이름 가져오고 검색어 필터링
    status, school_name = query_filter(school_name=request.args.get("school_name", ""))

    # 검색어가 필터링된 경우
    if not status:
        return error(code="school.query_filtered")

    # 학교 검색 결과 불러오기
    result = get_school_data_by_query(query=school_name)

    if result is None:
        # API 서버에서 받은 정보가 없으면
        return error(code="school.result_none")
    elif result is False:
        # 교육청 점검 or 타임아웃
        return error(code="school.api_timeout_or_dead")

    # 검색 결과가 있으면 학교 목록 리턴
    return jsonify(result)


@bp.get("/meal")
def meal():
    edu_code = request.args.get("edu", None)
    school_code = request.args.get("school", None)
    date = request.args.get("date", datetime.now().strftime("%Y%m%d"))

    if edu_code is None or school_code is None:
        return error(code="meal.query_none")

    result = get_meal_data_by_codes(
        edu=edu_code,
        school=school_code,
        date=date
    )

    if result is None or result == []:
        # API 서버에서 받은 정보가 없으면 ( 급식 없는 날 / 주말 / 휴교일 )
        return error(code="meal.result_none")
    elif result is False:
        # 교육청 점검 or 타임아웃
        return error(code="meal.timeout_or_dead")

    # 급식 출력하기
    return jsonify(result)
