# -*- coding: utf-8 -*-
from random import choice

from flask import Blueprint
from flask import session
from flask import render_template


bp = Blueprint(
    name="index",
    import_name="index",
    url_prefix="/"
)


@bp.get("/")
def index():
    try:
        alert = session['alert']
        del session['alert']
    except KeyError:
        alert = None

    return render_template(
        "index/index.html",
        title="급식",
        placeholder=choice(["ㅇㅇ초",       "ㅇㅇ중",     "ㅇㅇ고",
                            "ㅇㅇ초등학교", "ㅇㅇ중학교", "ㅇㅇ고등학교",
                            "ㅁㅁ초",       "ㅁㅁ중",     "ㅁㅁ고",
                            "ㅁㅁ초등학교", "ㅁㅁ중학교", "ㅁㅁ고등학교"]),

        alert=alert
    )
