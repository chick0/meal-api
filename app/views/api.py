# -*- coding: utf-8 -*-
from json import dumps
from random import choice

from flask import Blueprint
from flask import request
from flask import Response, url_for

import read


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


@bp.route("/get")
def get_poem():
    # 등록된 시 중에서 한 가지 추출
    ctx = getattr(read, choice(read.__all__))

    # 작품에서 한 구절 랜점 추첨
    preview = choice([text for text in ctx.CONTENT if len(text) != 0]).replace("&nbsp;", "")

    # 급식 세션 아이디 가져오기
    idx = request.args.get("idx", "none")

    # 해당 세션 아이디가 규칙을 따르는지 검사 ( s로 시작하는가 , 5자 인가 )
    if not idx.startswith("s") or len(idx) != 5:
        idx = None

    return Response(
        status=200,
        mimetype="application/json",
        response=dumps({
            "url": url_for("read.show", author=ctx.AUTHOR, title=ctx.TITLE, idx=idx),
            "preview": preview
        })
    )
