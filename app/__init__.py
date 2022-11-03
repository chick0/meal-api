from os import environ
from os.path import join
from os.path import abspath
from os.path import dirname

from flask import Flask
from flask import Response
from flask import send_from_directory
from werkzeug.exceptions import NotFound
from redis import Redis
from dotenv import load_dotenv

if "REDIS_URL" not in environ:
    load_dotenv()


def create_app():
    app = Flask(__name__, static_folder=None)

    REDIS_URL = environ.get("REDIS_URL", default=None)

    if REDIS_URL is None:
        app.redis = None
    else:
        app.redis = Redis.from_url(
            url=REDIS_URL
        )

    API_KEY = environ.get("API_KEY", default="#")

    if API_KEY == "#":
        raise Exception("시작할 수 없습니다. '나이스 교육정보 개방 포털'의 API 키가 필요합니다.")

    app.API_KEY = API_KEY

    from app.routes import api
    app.register_blueprint(api.bp)

    BASE_DIR = dirname(dirname(abspath(__file__)))
    DIST_DIR = join(BASE_DIR, "dist")

    @app.get("/")
    @app.get("/<path:path>")
    def frontend(path = None):  # noqa: E251
        if path is None:
            path = "index.html"

        try:
            response: Response = send_from_directory(
                directory=DIST_DIR,
                path=path
            )
        except NotFound:
            return "파일을 찾을 수 없습니다.", 404

        if path.endswith(".js"):
            response.content_type = "text/javascript; charset=utf-8"

        return response

    return app
