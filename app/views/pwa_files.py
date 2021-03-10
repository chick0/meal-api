# -*- coding: utf-8 -*-

from flask import Blueprint, send_file


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix="/"
)


@bp.route("/manifest.json")
def pwa_manifest():
    return send_file(
        mimetype="application/json",
        filename_or_fp="static/pwa/manifest.json"
    )


@bp.route("/service-worker.js")
def pwa_service_worker():
    return send_file(
        mimetype="application/javascript",
        filename_or_fp="static/pwa/service-worker.js"
    )
