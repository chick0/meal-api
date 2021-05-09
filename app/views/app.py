# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


@bp.route("/no-network")  # 오프라인 화면
def no_network():
    return render_template(
        "app/no_network.html",
        title="인터넷 연결 없음"
    ), 200


@bp.route("/tool")
def tool():
    return render_template(
        "app/tool.html",
        title="🌟 즐겨찾기 관리자"
    )


@bp.route("")
def start_page():
    return render_template(
        "app/start_page.html",
        title="🌟 즐겨찾기"
    )


# # # # # # # # # # # # # # # # # # #
@bp.route("/admin")
def admin():
    return render_template(
        "app/admin.html"
    )
