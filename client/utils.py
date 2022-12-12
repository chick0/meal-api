from json import loads

from .payload import to_query
from .request import fetch


def fetch_data(url: str, payload: dict) -> dict:
    query = to_query(**payload)

    response = fetch(url, query)

    return loads(response.read())


def search_school_by_name(school_name: str):
    return fetch_data(
        "https://open.neis.go.kr/hub/schoolInfo",
        {
            "SCHUL_NM": school_name
        }
    )


def search_meal_by_codes(edu: str, school: str, date: str):
    return fetch_data(
        "https://open.neis.go.kr/hub/mealServiceDietInfo",
        {
            "ATPT_OFCDC_SC_CODE": edu,
            "SD_SCHUL_CODE": school,
            "MLSV_YMD": date
        }
    )
