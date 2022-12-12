from urllib.parse import urlencode

from flask import current_app as app


def get_basic_payload() -> dict:
    return {
        "key": app.config['API_KEY'],
        "type": "json",
        "pIndex": 1,
        "pSize": 30,
    }


def to_query(**kwargs: dict) -> str:
    payload = get_basic_payload()

    for key, value in kwargs.items():
        payload[key] = value

    return urlencode(payload)
