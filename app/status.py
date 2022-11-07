from enum import Enum


class SearchMeal(Enum):
    API_REQUEST_FAIL = -1
    EMPTY_RESULT = -2


class SchoolSearch(Enum):
    WRONG_QUERY = 1
    API_REQUEST_FAIL = 2
    EMPTY_RESULT = 3
