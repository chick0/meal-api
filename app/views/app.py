from flask import Blueprint
from flask import render_template

bp = Blueprint(
    name="app",
    import_name="app",
    url_prefix="/app"
)


@bp.get("/no-network")
def no_network():
    return render_template(
        "app/no_network.html",
        title="인터넷 연결 없음"
    ), 200


@bp.get("")
def start_page():
    return render_template(
        "app/start_page.html",
        title="🌟 즐겨찾기"
    )
