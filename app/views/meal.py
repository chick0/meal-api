# -*- coding: utf-8 -*-

from datetime import datetime

from flask import Blueprint
from flask import redirect, url_for

from app.module import display

bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


@bp.route("/<string:edu_code>/<string:school_code>")
def show_today(edu_code: str, school_code: str):
    # 오늘 날짜 가져오기 - 서버 기준
    today = datetime.today()

    # 급식 출력하기
    return display.return_meal(
        date=today,                # 날짜 형식 YYYY MM DD 로 변환
        edu_code=edu_code,        # 교육청 코드
        school_code=school_code,  # 학교 코드
    )


@bp.route("/<string:edu_code>/<string:school_code>/<string:date>")
def show_custom_date(edu_code: str, school_code: str, date: str):
    # 오늘 날짜 가져오기 - 서버 기준
    today = datetime.today()

    # 오늘 급식은 이 뷰 포인트 이용 안함!
    if date == today.strftime('%Y%m%d'):
        return redirect(
            url_for(
                ".show_today",
                edu_code=edu_code,
                school_code=school_code
            )
        )

    # 급식 출력하기
    return display.return_meal(
        date=date,                # 날짜 값 그대로 전송
        edu_code=edu_code,        # 교육청 코드
        school_code=school_code,  # 학교 코드
    )
