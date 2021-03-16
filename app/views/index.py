# -*- coding: utf-8 -*-
from random import choice

from flask import Blueprint, session
from flask import render_template


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix="/"
)


@bp.route("/")
def index():
    try:
        alert = session['alert']
        del session['alert']
    except KeyError:
        alert = None

    # 모든 학교 세션 아이디 삭제
    for key in [key for key in session.keys() if key.startswith("s")]:
        del session[key]

    return render_template(
        "index/index.html",
        title="급식",
        placeholder=choice(["ㅇㅇ초",       "ㅇㅇ중",     "ㅇㅇ고",
                            "ㅇㅇ초등학교", "ㅇㅇ중학교", "ㅇㅇ고등학교",
                            "ㅁㅁ초",       "ㅁㅁ중",     "ㅁㅁ고",
                            "ㅁㅁ초등학교", "ㅁㅁ중학교", "ㅁㅁ고등학교"]),

        alert=alert
    )
