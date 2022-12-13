from os import environ
from sys import exit
from logging import getLogger

from flask import Flask
from flask import g
from redis import Redis

logger = getLogger()


def create_app():
    app = Flask(__name__, static_folder=None)

    try:
        app.config['API_KEY'] = environ['API_KEY'].strip()
    except KeyError:
        logger.error("'나이스 교육정보 개방 포털'의 API 키가 환경 변수에 없습니다.")
        exit(-1)

    try:
        redis = Redis.from_url(app.config['REDIS_URL'].strip())
    except KeyError:
        logger.warning("REDIS_URL이 환경 변수에 없습니다! redis 캐싱을 사용하지 않습니다.")
        redis = None

    @app.before_request
    def before_request():
        g.redis = redis

    from app.routes import api
    app.register_blueprint(api.bp)

    app.register_error_handler(
        404,
        lambda error: ({
            "code": "404",
            "message": "올바른 경로가 아닙니다."
        }, error.code)
    )

    return app
