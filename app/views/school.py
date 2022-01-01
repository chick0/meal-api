from flask import Blueprint
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import render_template

from app.search import query_filter
from app.search import get_school_data_by_query

bp = Blueprint(
    name="school",
    import_name="school",
    url_prefix="/school"
)


def alert(msg: str):
    session['alert'] = msg
    return redirect(url_for("index.index"))


@bp.post("")
def select():
    # 학교 이름 가져오고 검색어 필터링
    status, school_name = query_filter(school_name=request.form.get("school_name", ""))

    # 검색어가 필터링된 경우
    if not status:
        return alert(msg="해당 검색어는 사용이 불가능 합니다")

    # 학교 검색 결과 불러오기
    result = get_school_data_by_query(query=school_name)

    if result is None:
        # API 서버에서 받은 정보가 없으면
        return alert(msg="검색 결과가 없습니다")
    elif result is False:
        # 교육청 점검 or 타임아웃
        return alert(msg="학교 목록을 불러오는 데 실패했습니다")

    # 검색 결과가 있으면 학교 선택
    return render_template(
        "school/select.html",
        title="학교 선택",
        result=result
    )
