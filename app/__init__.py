
from flask import Flask
from flask_redis import FlaskRedis

from . import error
from . import config

redis = FlaskRedis()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # Redis 캐시 서버
    if not app.config.get("NO_REDIS"):
        redis.init_app(app)

    @app.after_request
    def set_header(response):
        response.headers['X-Frame-Options'] = "deny"
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
