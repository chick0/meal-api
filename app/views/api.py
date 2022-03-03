from datetime import datetime

from flask import Blueprint
from flask import request
from flask import jsonify

from app.search import query_filter
from app.search import get_school_data_by_query
from app.meal import get_meal_data_by_codes
from app.const import ERRORS

bp = Blueprint(
    name="api",
    import_name="api",
    url_prefix="/api"
)


def error(code: str):
    tp, cd = code.split(".")
    message = ERRORS.get(tp, {}).get(cd, "등록되지 않은 오류입니다. 개발자한테 신고해주세요.")

    return jsonify({
        "code": code,
        "message": message
    }), 400


@bp.get("/errors")
def errors():
    return jsonify(ERRORS)


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
    # 오늘 날짜 불러오기
    #  -> 시간은 버리기
    date_format = "%Y" + "%m" + "%d"
    today = datetime.strptime(datetime.today().strftime(date_format), date_format)

    # 교육청 코드 & 학교 코드 불러오기
    edu_code = request.args.get("edu", None)
    school_code = request.args.get("school", None)

    # 조회 요청에 교육청 코드 또는 학교 코드가 없다면
    if edu_code is None or school_code is None:
        return error(code="meal.query_none")

    # 조회 날짜 날짜 불러오기
    date = request.args.get("date", None)

    # 조회 날짜를 설정하지 않았다면 오늘 날짜로 설정하기
    if date is None:
        date = today.strftime(date_format)

    # 날짜 형식이 올바르지 않다면
    if len(date) != 8:
        return error(code="meal.not_yyyymmdd")

    # 데이터 불러오기
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
        return error(code="meal.api_timeout_or_dead")

    # 급식 출력하기
    return jsonify(result)
