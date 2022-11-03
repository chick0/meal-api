from importlib import import_module

from flask import Blueprint

bp = Blueprint("api", __name__, url_prefix="/api")

import_module("app.routes.meal")
import_module("app.routes.school")
