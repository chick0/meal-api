from json import dumps
from json import loads
from urllib.error import HTTPError
from typing import Union
from typing import Optional
from logging import getLogger

from flask import g
from redis.exceptions import ConnectionError

from app.reformat import reformat
from app.status import SearchMeal
from client.utils import search_meal_by_codes

logger = getLogger()


def format_name(name: str) -> str:
    return "(" + name.replace("#", ", ") + ")"


def fetch_from_redis(name: str) -> Optional[list]:
    if g.redis is None:
        return None

    try:
        from_redis = g.redis.get(name)

        if from_redis is None:
            return None

        logger.info(f"Get meal data from redis {format_name(name)}")
        return loads(from_redis)
    except ConnectionError:
        logger.error("redis server connection failed")
    except TypeError:
        pass
    except Exception:
        logger.exception("Exception in getting data from redis")


def add_cache(name: str, json: list):
    try:
        g.redis.set(
            name=name,
            value=dumps(json),
            ex=604800
        )

        logger.info(f"Add meal data to redis {format_name(name)}")
    except ConnectionError:
        logger.error("redis server connection failed")


def fetch_from_api(edu: str, school: str, date: str) -> Optional[dict]:
    try:
        return search_meal_by_codes(edu, school, date)
    except HTTPError:
        logger.exception("NEIS Open API request has been failed.")
    except Exception:
        logger.exception("Exception in meal data api request")


def get_meal_data_by_codes(edu: str, school: str, date: str) -> Union[SearchMeal, list]:
    name = f"{edu}#{school}#{date}"

    result = fetch_from_redis(name)

    if result is None:
        logger.info(f"Get meal data from api {format_name(name)}")

        result = fetch_from_api(edu, school, date)

        if result is None:
            return SearchMeal.API_REQUEST_FAIL

        try:
            result = [j['row'] for j in [i for i in result['mealServiceDietInfo']] if "row" in j][0]
        except KeyError:
            return SearchMeal.EMPTY_RESULT

        result = reformat(result)

        if g.redis is not None:
            add_cache(name, result)

    return result
