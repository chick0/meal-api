# -*- coding: utf-8 -*-
from io import BytesIO

from flask import Flask, g
from flask import send_file
from flask_redis import FlaskRedis

from app.module import error
from conf import conf


redis = FlaskRedis()


def create_app():
    app = Flask(__name__)

    # Redis 데이터베이스
    app.config['REDIS_URL'] = conf['redis']['url']
    redis.init_app(app)

    # 세션 용 시크릿 키
    try:
        app.config['SECRET_KEY'] = open(".SECRET_KEY", mode="rb").read()
    except FileNotFoundError:
        from secrets import token_bytes
        app.config['SECRET_KEY'] = token_bytes(32)
        open(".SECRET_KEY", mode="wb").write(app.config['SECRET_KEY'])

    # 세션 쿠키 설정
    app.config['SESSION_COOKIE_NAME'] = "s"
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = "Strict"

    @app.route("/favicon.ico")
    def favicon():
        return send_file(
            "static/img/favicon.ico",
            mimetype="image/x-icon"
        )

    @app.route("/robots.txt")
    def robots():
        return send_file(
            BytesIO(b"\n".join([
                b"User-agent: *",
                b"Allow: /$",       # 메인 페이지
                b"Allow: /static",  # js, css, img 같은 정적 파일들
                b"Disallow: /",     # 위를 제외한 나머지 다
            ])),
            mimetype="text/plain"
        )

    @app.route("/manifest.json")
    def manifest():
        return send_file(
            "static/pwa/manifest.json",
            mimetype="application/json"
        )

    @app.route("/service-worker.js")
    def service_worker():
        return send_file(
            "static/pwa/service-worker.js",
            mimetype="application/javascript"
        )

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
        app.register_blueprint(
            blueprint=getattr(getattr(views, view_point), "bp")
        )

    # 오류 핸들러
    app.register_error_handler(400, error.bad_request)
    app.register_error_handler(403, error.forbidden)
    app.register_error_handler(404, error.page_not_found)
    app.register_error_handler(405, error.method_not_allowed)

    app.register_error_handler(500, error.internal_server_error)

    return app
