# -*- coding: utf-8 -*-
from os import path
from re import compile
from io import StringIO

from flask import Flask
from flask import request, g
from flask import send_file
from flask_redis import FlaskRedis

from app.module import error, template_filter
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
            mimetype="text/plain",
            filename_or_fp=StringIO("\n".join([
                "User-agent: *",
                "Allow: /$",
                "Allow: /static",
                "Allow: /read",
                "Disallow: /",
            ]))
        )

    @app.before_first_request
    def set_pwa_service_worker_version():
        try:
            with open(path.join("app", "static", "pwa", "service-worker.js"), mode="r", encoding="utf-8") as fp:
                js = fp.read()

                pattern = compile(r"const CACHE_VER = \"([0-9]{4}-[0-9]{2}-[0-9]{2}_v[0-9]{2,})\";")
                worker_version = pattern.findall(js)[0]
        except FileNotFoundError:
            worker_version = "undefined"

        redis.set("pwa_service_worker_version", worker_version)

    @app.before_request
    def for_uptime_bot():
        if "Uptime" in request.user_agent.string:
            return "OK", 200

    @app.before_request
    def ban():
        ban_keywords = [
            "curl",
            "python-requests",
            "Python-urllib",
            "Scrapy",
            "axios",
            "Nutch",
            "Go-http-client",
        ]

        for keyword in ban_keywords:
            if keyword in request.user_agent.string:
                return "", 200

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
        response.headers['X-XSS-Protection'] = "1"    # Cross-site scripting

        response.headers['X-Powered-By'] = "chick_0"
        return response

    # Redis 초기화
    redis.init_app(app)

    # 템플릿 필터 등록
    app.add_template_filter(template_filter.origin)
    app.add_template_filter(template_filter.parse_menu)
    app.add_template_filter(template_filter.allergy)

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
