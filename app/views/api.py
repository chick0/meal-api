# -*- coding: utf-8 -*-
from json import dumps
from random import choice

from flask import Blueprint, session
from flask import Response, redirect, url_for

from sqlalchemy.exc import OperationalError

from models import Poem


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


def get_preview_from_ctx(ctx: Poem):
    # `\n`을 기준으로 줄 바꿈
    content = ctx.content.split("\n")

    # 작품에서 한 구절 랜점 추첨
    preview = choice(content)

    if len(preview.strip()) != 0:  # 공백이 아닐 경우
        return preview
    else:                          # 공백이면 다시 추첨
        return get_preview_from_ctx(ctx=ctx)


@bp.route("/")
def index():
    session['alert'] = "그 아이가 내게 옷걸이를 던졌다고요."
    return redirect(url_for("index.index"))


@bp.route("/get")
@bp.route("/get/<string:idx>")
def get_poem(idx: str = None):
    try:
        ctx = choice(Poem.query.all())
    except (OperationalError, Exception):  # DB 접속 실패
        return Response(
            status=500,
            mimetype="application/json",
            response="""{"msg": "database connection error"}"""
        )

    if ctx is not None:
        status = 200
        preview = get_preview_from_ctx(ctx=ctx)
        url = url_for("read.show", author=ctx.author, title=ctx.title, idx=idx)
    else:
        status = 404
        preview = "등록된 작품이 없습니다"
        url = "#"

    return Response(
        status=status,  # 200 or 404
        mimetype="application/json",
        response=dumps(
            dict(
                url=url,
                preview=preview
            )
        )
    )
