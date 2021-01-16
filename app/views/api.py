# -*- coding: utf-8 -*-
from json import dumps

from flask import Blueprint, session
from flask import Response, redirect, url_for

from sqlalchemy.exc import OperationalError

from app.module.poem import get_list, get_ctx_by_metadata
from app.module.poem import get_random_ctx, get_preview_from_ctx

bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


@bp.route("/")
def index():
    session['alert'] = "그 아이가 내게 옷걸이를 던졌다고요."
    return redirect(url_for("index.index"))


@bp.route("/fetch/list")
def fetch_poem_list():
    try:
        ctx = get_list()
    except (OperationalError, Exception):  # DB 접속 실패
        return Response(
            status=500,
            mimetype="application/json",
            response="""{"msg": "database connection error"}"""
        )

    return Response(
        status=200,
        mimetype="application/json",
        response=dumps(
            obj=ctx
        )
    )


@bp.route("/fetch/<string:author>/<string:title>")
def fetch_poem(author, title):
    try:
        ctx = get_ctx_by_metadata(author=author, title=title)
    except (OperationalError, Exception):  # DB 접속 실패
        return Response(
            status=500,
            mimetype="application/json",
            response="""{"msg": "database connection error"}"""
        )

    if ctx is not None:
        status = 200
        content = ctx.content.split("#")
    else:
        status = 404
        content = []

    return Response(
        status=status,  # 200 or 404
        mimetype="application/json",
        response=dumps(
            obj=content
        )
    )


@bp.route("/get")
@bp.route("/get/<string:idx>")
def get_poem(idx: str = None):
    try:
        ctx = get_random_ctx()
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
        url = url_for("index.index")

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
