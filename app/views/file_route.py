# -*- coding: utf-8 -*-

from flask import Blueprint, send_file

bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix="/"
)


# ROBOTS
@bp.route("/robots.txt")
def robots():
    return send_file(
        mimetype="text/plain",
        filename_or_fp=StringIO("\n".join([
            "User-agent: *",
            "Allow: /$",
            "Allow: /static",
            "Allow: /read",
            "Disallow: /",
        ]))
    )


# ICON
@bp.route("/favicon.ico")
def favicon():
    return send_file(
        "static/img/favicon.ico",
        mimetype="image/x-icon"
    )


# PWA
@bp.route("/manifest.json")
def pwa_manifest():
    return send_file(
        "static/pwa/manifest.json",
        mimetype="application/json"
    )


@bp.route("/service-worker.js")
def pwa_service_worker():
    return send_file(
        "static/pwa/service-worker.js",
        mimetype="application/javascript"
    )
