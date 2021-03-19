# -*- coding: utf-8 -*-
from os import path
from io import StringIO

from flask import Flask
from flask import request, g
from flask import send_file
from flask_redis import FlaskRedis

from app.module import error
from conf import conf


redis = FlaskRedis()


def create_app():
    app = Flask(__name__)
    app.config.from_object(obj=__import__("config"))

    @app.route("/favicon.ico")
    def favicon():
        return send_file(
            "static/img/favicon.ico",
            mimetype="image/x-icon"
        )

    @app.route("/robots.txt")
    def robots():
        return send_file(
            StringIO("\n".join([
                "User-agent: *",
                "Allow: /$",       # 메인 페이지
                "Allow: /static",  # js, css, img 같은 동적 파일들
                "Allow: /read",    # 시
                "Disallow: /",     # 위를 제외한 나머지 다
            ])),
            mimetype="text/plain"
        )

    @app.before_first_request
    def set_pwa_service_worker_version():
        try:
            # 서비스 워커 스크립트 읽어오기
            with open(path.join("app", "static", "pwa", "service-worker.js"), mode="r", encoding="utf-8") as fp:
                # 1,2 번줄은 스킵
                fp.readline(), fp.readline()

                # 3 번째 줄에서 버전 정보 읽어오기
                worker_version = fp.readline().split('const CACHE_VER = "')[-1][:-3]
        except FileNotFoundError:
            worker_version = "undefined"

        redis.set("pwa_service_worker_version", worker_version)

    @app.before_request
    def for_uptime_bot():
        if "Uptime" in request.user_agent.string:
            return "OK", 200

    @app.before_request
    def set_global():
        # 웹사이트 도메인
        g.host = conf['app']['host']

        # 카카오톡 자바스크립트 API 키
        g.k = conf['api']['k']
        # 카카오톡 공유하기 템플릿 ID
        g.tid = conf['api']['tid']

    @app.after_request
    def set_header(response):
        response.headers['X-Frame-Options'] = "deny"  # Clickjacking
        response.headers['X-Powered-By'] = "chick_0"
        return response

    # Redis 초기화
    redis.init_app(app)

    # 국내산 확인용 필터
    # 1) 텍스트에서 ':'을 기준으로 식재료와 원산지 정보로 분리
    # 2) 원산지 정보에서 '국내산' 제거
    # 3) 제거된 원산진 정보에서 '산' 이 있는지 확인
    # 4-1) 있다면, 수입산이 포함된 식재료
    # 4-2) 없다면, 국내산만 포함된 식재료
    app.add_template_filter(
        lambda s: s.split(":")[-1].replace("국내산", "").find("산") == -1,
        name="origin"
    )

    from app import views
    for view_point in views.__all__:
        try:
            app.register_blueprint(   # 블루프린트 등록시도
                blueprint=getattr(getattr(views, view_point), "bp")
            )
        except AttributeError:        # 블루프린트 객체가 없다면
            print(f"[!] '{view_point}' 는 뷰 포인트가 아닙니다")

    # 오류 핸들러
    app.register_error_handler(400, error.bad_request)
    app.register_error_handler(403, error.forbidden)
    app.register_error_handler(404, error.page_not_found)
    app.register_error_handler(405, error.method_not_allowed)

    app.register_error_handler(500, error.internal_server_error)

    return app
