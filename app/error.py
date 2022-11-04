ERRORS = {
    "school": {
        "query_filtered": "해당 검색어는 사용할 수 없습니다.",
        "result_none": "검색 결과가 없습니다.",
        "api_timeout_or_dead": "학교 목록을 불러오는 데 실패했습니다.",
    },
    "meal": {
        "result_none": "급식 정보가 없습니다.",
        "api_timeout_or_dead": "급식 정보를 불러오는 데 실패했습니다.",
        "query_none": "요청오류) 교육청 코드와 학교 코드를 전달받지 못했습니다.",
        "not_yyyymmdd": "요청오류) 요청 날짜의 YYYYMMDD 형식을 지켜주세요."
    },
}


def error(code: str):
    tp, cd = code.split(".")
    message = ERRORS.get(tp, {}).get(cd, "등록되지 않은 오류입니다.")

    return {
        "code": code,
        "message": message
    }, 400
