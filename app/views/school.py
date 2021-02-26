# -*- coding: utf-8 -*-
from re import findall

from flask import abort
from flask import Blueprint, request, session
from flask import render_template
from flask import redirect, url_for

from app.module.api import search_school_by_name

bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


def alert(msg: str):
    session['alert'] = msg
    return redirect(url_for("index.index"))


@bp.route("/select", methods=['GET', 'POST'])
def select():
    # 출발지 검사 & HTTP 메소드 검사
    if request.referrer is None or request.method != "POST":
        abort(405)

    # 검색어가 없는 경우
    if school_name is None or len(school_name) == 0:
        return alert(msg="검색어를 입력해주세요")

    # ----------------------------------------------------------- #
    if school_name == "chick_0" or school_name == "ch1ck_0":
        session['alert'] = "(~˘▾˘)~♫•*¨*•.¸¸♪"
        return redirect(url_for("index.index"))
    # ----------------------------------------------------------- #

    # 필터링
    school_name = "".join(findall("[가-힣]", school_name))

    # 필터링후 검색어가 0글자 이면, 공백 검색어로 분류
    if len(school_name) == 0:
        return alert(msg="한국어로만 검색할 수 있습니다")

    # 금지된 검색어들
    if school_name in ["초등", "초등학교", "중", "중학교", "고등", "고등학교", "학교"]:
        return alert(msg="해당 검색어는 사용이 불가능 합니다")

    # 검색어로 학교 찾기
    try:
        school_list, status_code = search_school_by_name(
            school_name=school_name
        )
    except (ValueError, Exception):
        return alert(msg="학교 목록을 불러오는 데 실패했습니다")

    if status_code == 200:  # API 서버에서 200응답을 받았다면?
        try:                           # 검색 결과가 있으면 학교 선택
            return render_template(
                "school/select.html",
                title="학교 선택",
                result=school_list['schoolInfo'][1]['row']
            )
        except (KeyError, Exception):  # 없으면 검색 결과가 없음
            return alert(msg="검색 결과가 없습니다")
    else:                   # 아니면, API 오류!
        return alert(msg="학교 목록을 불러오는 데 실패했습니다")
