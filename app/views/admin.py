# -*- coding: utf-8 -*-
from datetime import datetime

from flask import Blueprint
from flask import render_template
from flask import redirect, url_for

from app import redis


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


@bp.route("")
def index():
    keys = [key.decode() for key in redis.keys("*#*#*")]

    return render_template(
        "admin/index.html",
        title="캐싱된 급식 목록",

        keys=keys
    )


@bp.route("/delete")
def delete():
    keys = [
        key.decode() for key in redis.keys("*#*#*")

        # 이번달 급식을 제외하기
        if not key.decode().rsplit("#", 1)[-1].startswith(datetime.today().strftime("%Y%m"))
    ]

    # 저번달 혹은 다음달 급식 삭제하기
    for key in keys:
        redis.delete(key)

    return redirect(url_for(".index"))
