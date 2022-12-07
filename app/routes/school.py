from flask import request
from app.routes.api import bp

from app.error import error
from app.search import query_filter
from app.search import get_school_data_by_query
from app.status import SchoolSearch


@bp.get("/school")  # type: ignore
def search():
    # 학교 필터링
    school_name_from_args = request.args.get("school_name", "")
    school_name = query_filter(school_name_from_args)

    # 검색어가 필터링된 경우
    if school_name == SchoolSearch.WRONG_QUERY:
        return error(code="school.query_filtered")

    # 학교 검색 결과 불러오기
    result = get_school_data_by_query(query=school_name)  # type: ignore

    if result == SchoolSearch.EMPTY_RESULT:
        # API 서버에서 받은 정보가 없으면
        return error(code="school.result_none")

    if result == SchoolSearch.API_REQUEST_FAIL:
        # 교육청 점검 or 타임아웃
        return error(code="school.api_timeout_or_dead")

    # 검색 결과가 있으면 학교 목록 리턴
    return result
