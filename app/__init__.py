from json import load

from flask import Flask
from flask import request
from flask_redis import FlaskRedis

from . import error
from . import config
from . import template_filter

redis = FlaskRedis()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # 시 불러오기
    app.config.update({
        "poems": load(open("poems.json", mode="r", encoding="utf-8"))
    })

    # Redis 캐시 서버
    if not app.config.get("NO_REDIS"):
        redis.init_app(app)

    @app.after_request
    def set_header(response):
        response.headers['X-Frame-Options'] = "deny"
        response.headers['X-Powered-By'] = "chick_0"

        if request.path.startswith("/api/"):
            response.headers['Access-Control-Allow-Origin'] = "*"
            response.headers['Access-Control-Allow-Methods'] = "GET"

        return response

    for name in [x for x in dir(template_filter) if not x.startswith("__")]:
        func = getattr(template_filter, name)
        if func.__class__.__name__ == "function":
            app.add_template_filter(
                f=func, name=name
            )

    from . import views
    for view in views.__all__:
        app.register_blueprint(getattr(getattr(views, view), "bp"))

    # 오류 핸들러
    app.register_error_handler(400, error.bad_request)
    app.register_error_handler(403, error.forbidden)
    app.register_error_handler(404, error.page_not_found)
    app.register_error_handler(405, error.method_not_allowed)

    app.register_error_handler(500, error.internal_server_error)

    return app
