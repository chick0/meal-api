# -*- coding: utf-8 -*-
from json import loads, dumps
from random import choice

from flask import Blueprint
from flask import Response

from app import redis

bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


@bp.route("/read")
def read():
    ctx = loads(redis.get(choice(redis.keys("api_read_*"))))
    return Response(
        status=200,
        mimetype="application/json",
        response=dumps(dict(
            a=ctx.get("a"), b=ctx.get("b")
        ))
    )
