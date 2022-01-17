from random import choice
from datetime import datetime

from flask import Blueprint
from flask import current_app
from flask import session
from flask import abort
from flask import redirect
from flask import url_for
from flask import render_template

from app.meal import get_meal_data_by_codes
from app.weeks import Day

bp = Blueprint(
    name="meal",
    import_name="meal",
    url_prefix="/meal"
)


@bp.get("/<string:edu_code>/<string:school_code>/")
@bp.get("/<string:edu_code>/<string:school_code>/<string:date>")
def show(edu_code: str, school_code: str, date: str = "today"):
    # 오늘 날짜 불러오기
    #  -> 시간은 버리기
    date_format = "%Y" + "%m" + "%d"
    today = datetime.strptime(datetime.today().strftime(date_format), date_format)

    if date == "today":
        # 급식 조회할 날짜를 오늘 날짜로 설정하기
        day = today
    else:
        try:
            # URL에서 급식 조회할 날짜 불러오기
            day = datetime.strptime(date, date_format)

            # 오늘 날짜면 today 링크로 리다이렉트
            if day.date() == datetime.today().date():
                return redirect(url_for(".show", edu_code=edu_code, school_code=school_code, date="today"))
        except ValueError:
            # 전달받은 날짜로 날짜를 불러오지 못함
            return abort(400)

    # 시 불러오기
    poems = current_app.config.get("poems")
    poem_id = choice(list(poems.keys()))

    poem = poems.get(poem_id, {})
    p_text = choice([x.replace("&nbsp;", "") for x in poem.get("content", "") if len(x.strip()) != 0])

    # 조회 날짜가 30일 보다 먼 미래인 경우
    if (day - today).days >= 30:
        return render_template(
            "meal/blocked.html",
            title="조회 요청 거부",

            day=day,

            edu_code=edu_code,        # 교육청 코드
            school_code=school_code,  # 학교 코드

            poem_id=poem_id,              # 시 고유 코드
            p_text=p_text,                # 시 [한줄만]
            p_title=poem.get("title"),    # 제목
            p_author=poem.get("author"),  # 작가
        )

    # 이번주 이동 버튼
    weeks = Day(dt=day).get_center(length=5)

    # 교육청 코드와 학교 코드와 날짜로 급식 불러오기
    result = get_meal_data_by_codes(
        edu=edu_code,
        school=school_code,
        date=day.strftime(date_format)
    )

    if result is None or result == []:
        # API 서버에서 받은 정보가 없으면 ( 급식 없는 날 / 주말 / 휴교일 )
        return render_template(
            "meal/not_found.html",
            title="정보 없음",

            day=day,
            today=today,

            edu_code=edu_code,        # 교육청 코드
            school_code=school_code,  # 학교 코드

            poem_id=poem_id,              # 시 고유 코드
            p_text=p_text,                # 시 [한줄만]
            p_title=poem.get("title"),    # 제목
            p_author=poem.get("author"),  # 작가

            weeks=weeks,              # 이번주 급식 메뉴 이동 버튼용
        )
    elif result is False:
        # 교육청 점검 or 타임아웃
        session['alert'] = "급식 정보를 불러오는 데 실패했습니다"
        return redirect(url_for("index.index"))

    # 급식 출력하기
    return render_template(
        "meal/show.html",
        title=result[0]['school'],  # 학교 이름

        day=day,
        today=today,

        result=result,                # 급식 조회 결과
        edu_code=edu_code,            # 교육청 코드
        school_code=school_code,      # 학교 코드

        poem_id=poem_id,              # 시 고유 코드
        p_text=p_text,                # 시 [한줄만]
        p_title=poem.get("title"),    # 제목
        p_author=poem.get("author"),  # 작가

        weeks=weeks,                  # 이번주 급식 메뉴 이동 버튼용
    )
