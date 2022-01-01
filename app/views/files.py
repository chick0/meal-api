from flask import Blueprint
from flask import Response
from flask import send_file

bp = Blueprint(
    name="files",
    import_name="files",
    url_prefix="/"
)


@bp.route("/robots.txt")
def robots():
    return Response(
        "\n".join([
            "User-agent: *",
            "Allow: /$",
            "Disallow: /",
        ]),
        mimetype="text/plain"
    )


@bp.route("/favicon.ico")
def favicon():
    return send_file(
        "static/img/favicon.ico",
        mimetype="image/x-icon"
    )


@bp.route("/manifest.json")
def manifest():
    return send_file(
        "static/pwa/manifest.json",
        mimetype="application/json"
    )


@bp.route("/sw.js")
def service_worker():
    return send_file(
        "static/pwa/service-worker.js",
        mimetype="application/javascript"
    )
