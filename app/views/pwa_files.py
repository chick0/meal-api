# -*- coding: utf-8 -*-

from flask import Blueprint, send_file


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix="/"
)


@bp.route("/manifest.json")
def manifest():
    return send_file(
        "static/pwa/manifest.json",
        mimetype="application/json"
    )


@bp.route("/service-worker.js")
def service_worker():
    return send_file(
        "static/pwa/service-worker.js",
        mimetype="application/javascript"
    )
