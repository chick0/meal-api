from datetime import datetime
from datetime import timedelta

from flask import Blueprint
from flask import session
from flask import abort
from flask import redirect
from flask import url_for
from flask import render_template

from app.meal import get_meal_data_by_codes


bp = Blueprint(
    name="meal",
    import_name="meal",
    url_prefix="/meal"
)


@bp.get("/<string:edu_code>/<string:school_code>/")
@bp.get("/<string:edu_code>/<string:school_code>/<string:date>")
def show(edu_code: str, school_code: str, date: str = "today"):
    today = False

    if date == "today":
        # 오늘 날짜 불러오기
        day = datetime.today()
        date = day.strftime("%Y%m%d")

        today = True
    else:
        try:
            # 날짜 불러오기
            day = datetime.strptime(date, "%Y%m%d")

            # 오늘 날짜면 today 링크로 리다이렉트
            if day.date() == datetime.today().date():
                return redirect(url_for(".show", edu_code=edu_code, school_code=school_code, date="today"))
        except ValueError:
            # 전달받은 날짜로 날짜를 불러오지 못함
            return abort(400)

    # 내일 이동 버튼을 위한 값
    tomorrow = (day + timedelta(days=1)).strftime("%Y%m%d")

    # 어제 이동 버튼을 위한 값
    yesterday = (day - timedelta(days=1)).strftime("%Y%m%d")

    result = get_meal_data_by_codes(
        edu=edu_code,
        school=school_code,
        date=date
    )

    if result is None or result == []:
        # API 서버에서 받은 정보가 없으면 ( 급식 없는 날 / 주말 / 휴교일 )
        return render_template(
            "meal/not_found.html",
            title="정보 없음",

            day=day.strftime('%Y년 %m월 %d일'),

            edu_code=edu_code,        # 교육청 코드
            school_code=school_code,  # 학교 코드
            yesterday=yesterday,      # 어제
            tomorrow=tomorrow,        # 내일

            today=today               # 오늘 메뉴인지 검사용
        )
    elif result is False:
        # 교육청 점검 or 타임아웃
        session['alert'] = "급식 정보를 불러오는 데 실패했습니다"
        return redirect(url_for("index.index"))

    # 급식 출력하기
    return render_template(
        "meal/show.html",
        title=result[0]['school'],  # 학교 이름

        day=day.strftime('%Y년 %m월 %d일'),
        result=result,                # 급식 조회 결과

        edu_code=edu_code,            # 교육청 코드
        school_code=school_code,      # 학교 코드
        yesterday=yesterday,          # 어제
        tomorrow=tomorrow,            # 내일

        today=today,                  # 오늘 메뉴인지 검사용
    )
