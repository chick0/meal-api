# -*- coding: utf-8 -*-

from flask import Blueprint, session
from flask import render_template

bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix="/"
)


@bp.route("/ok")
def ok():
    return "OK", 200


@bp.route("/")
def index():
    try:
        alert = session['alert']
        del session['alert']
    except KeyError:
        alert = None

    return render_template(
        "index/index.html",
        title="급식",

        alert=alert
    )
