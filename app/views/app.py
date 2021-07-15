# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template


bp = Blueprint(
    name="app",
    import_name="app",
    url_prefix="/app"
)


@bp.route("/no-network")  # 오프라인 화면
def no_network():
    return render_template(
        "app/no_network.html",
        title="인터넷 연결 없음"
    ), 200


@bp.route("")
def start_page():
    return render_template(
        "app/start_page.html",
        title="🌟 즐겨찾기"
    )
