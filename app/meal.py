from json import dumps
from json import loads
from urllib.error import HTTPError
from logging import getLogger

from flask import current_app as app
from redis.exceptions import ConnectionError

from app.api import search_meal_by_codes
from app.reformat import reformat
from app.status import SearchMeal

logger = getLogger()


def fetch_from_redis(name: str) -> list or None:
    if app.redis is None:
        return None

    try:
        from_redis = app.redis.get(name)

        if from_redis is None:
            return None

        logger.info(f"Get meal data from Redis / {name}")
        return loads(from_redis)
    except ConnectionError:
        logger.error("Redis server connection failed")
    except TypeError:
        pass
    except Exception:
        logger.exception("Exception in getting data from Redis")


def add_cache(name: str, json: list):
    try:
        app.redis.set(
            name=name,
            value=dumps(json),
            ex=604800
        )

        logger.info(f"Add meal data to redis / {name}")
    except ConnectionError:
        logger.error("Redis server connection failed")


def fetch_from_api(edu: str, school: str, date: str) -> dict or None:
    try:
        return search_meal_by_codes(edu, school, date)
    except HTTPError:
        logger.exception("NEIS Open API request has been failed.")
    except Exception:
        logger.exception("Exception in meal data api request")


def get_meal_data_by_codes(edu: str, school: str, date: str) -> SearchMeal or list:
    name = f"{edu}#{school}#{date}"

    result = fetch_from_redis(name)

    if result is None:
        logger.info(f"Get meal data from api / {name}")

        result = fetch_from_api(edu, school, date)
        if result is None:
            return SearchMeal.API_REQUEST_FAIL

        try:
            result = [j['row'] for j in [i for i in result['mealServiceDietInfo']] if "row" in j][0]
        except KeyError:
            return SearchMeal.EMPTY_RESULT

        result = reformat(result)

        if app.redis is not None:
            add_cache(name, result)

    return result
