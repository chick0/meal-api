from datetime import datetime

from flask import request
from app.routes.api import bp

from app.error import error
from app.meal import get_meal_data_by_codes
from app.status import SearchMeal


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

    if result == SearchMeal.EMPTY_RESULT:
        # API 서버에서 받은 정보가 없으면 ( 급식 없는 날 / 주말 / 휴교일 )
        return error(code="meal.result_none")

    if result == SearchMeal.API_REQUEST_FAIL:
        # 교육청 점검 or 타임아웃
        return error(code="meal.api_timeout_or_dead")

    # 급식 출력하기
    return result
