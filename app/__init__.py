from os import environ
from sys import exit
from sys import stderr

from flask import Flask
from redis import Redis
from dotenv import load_dotenv

if "REDIS_URL" not in environ:
    load_dotenv()


def create_app():
    app = Flask(__name__, static_folder=None)

    REDIS_URL = environ.get("REDIS_URL", default=None)

    if REDIS_URL is None:
        app.redis = None  # type: ignore
    else:
        app.redis = Redis.from_url(  # type: ignore
            url=REDIS_URL
        )

    API_KEY = environ.get("API_KEY", default="#")

    if API_KEY == "#":
        stderr.write("API 서버를 시작할 수 없습니다. '나이스 교육정보 개방 포털'의 API 키가 필요합니다.")
        exit(-1)

    app.API_KEY = API_KEY  # type: ignore

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
