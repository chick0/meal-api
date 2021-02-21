# -*- coding: utf-8 -*-
from json import dumps
from random import choice

from flask import Blueprint
from flask import request, session
from flask import Response, redirect, url_for

import read


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


def get_preview(content: list):
    # 작품에서 한 구절 랜점 추첨
    preview = choice(content).replace("&nbsp;", "")

    if len(preview.strip()) != 0:  # 공백이 아닐 경우
        return preview
    else:                          # 공백이면 다시 추첨
        return get_preview(content)


@bp.route("/")
def index():
    session['alert'] = "그 아이가 내게 옷걸이를 던졌다고요."
    return redirect(url_for("index.index"))


@bp.route("/get")
def get_poem():
    ctx = getattr(read, choice(read.__all__))

    preview = get_preview(content=ctx.CONTENT)
    url = url_for("read.show", author=ctx.AUTHOR, title=ctx.TITLE)

    if request.args.get("idx") is not None:
        url += "?idx=" + request.args.get("idx")

    return Response(
        status=200,
        mimetype="application/json",
        response=dumps(
            dict(
                url=url,
                preview=preview
            )
        )
    )
