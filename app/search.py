from re import findall
from urllib.error import HTTPError
from typing import Union
from typing import Optional
from logging import getLogger

from app.status import SchoolSearch
from client.utils import search_school_by_name

logger = getLogger()


# 검색어 필터링
def query_filter(school_name: str) -> Union[SchoolSearch, str]:
    # 한글 완성자만 남기기
    school_name = "".join(findall("[가-힣]", school_name))

    # 검색어가 0글자 이하인지 확인
    if len(school_name) == 0:
        return SchoolSearch.WRONG_QUERY

    # 검색어가 금지어인 경우 확인
    if school_name in ["초등", "초등학교", "중", "중학교", "고등", "고등학교", "학교"]:
        return SchoolSearch.WRONG_QUERY

    return school_name


def fetch_from_api(query: str) -> Optional[dict]:
    try:
        return search_school_by_name(
            school_name=query
        )
    except HTTPError:
        logger.exception("NEIS Open API request has been failed.")
    except Exception:
        logger.exception("Exception in school search api request")


# 검색 기록 불러오기
def get_school_data_by_query(query: str) -> Union[SchoolSearch, list]:
    logger.info(f"School search requested {query!r}")
    result = fetch_from_api(query)

    if result is None:
        return SchoolSearch.API_REQUEST_FAIL

    try:
        result = [
            {
                "name": f"({school['LCTN_SC_NM']}) {school['SCHUL_NM']}",
                "code": {
                    "edu": school['ATPT_OFCDC_SC_CODE'],
                    "school": school['SD_SCHUL_CODE']
                }
            } for school in result['schoolInfo'][1]['row']
        ]

        return result
    except KeyError:
        """
        {'RESULT': {'CODE': 'INFO-200', 'MESSAGE': '해당하는 데이터가 없습니다.'}}
        """
        return SchoolSearch.EMPTY_RESULT
