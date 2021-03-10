# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template

from app import redis


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


@bp.route("/no-network.page")  # PWA 오프라인시 보이는 화면
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


@bp.route("/cache")
def cache():
    # 첫 번째 요청에서 확인한 PWA 서비스 워커 버전 정보 불러오기
    ver = redis.get("pwa_service_worker_version").decode()

    return render_template(
        "app/cache.html",
        title="서비스워커 캐시 버전",
        ver_server=ver
    )


@bp.route("")
def start_page():
    return render_template(
        "app/start_page.html",
        title="🌟 즐겨찾기"
    )
