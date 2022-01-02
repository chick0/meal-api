def origin(s: str) -> bool:
    # 국내산 확인용 필터
    #  1) 텍스트에서 ':'을 기준으로 식재료와 원산지 정보로 분리
    #  2) 원산지 정보에서 '국내산' 제거
    #  3) 제거된 원산진 정보에서 '산' 이 있는지 확인
    #     3-1) 있다면, 수입산이 포함된 식재료
    #     3-2) 없다면, 국내산만 포함된 식재료*

    return s.split(":")[-1].replace("국내산", "").find("산") == -1


def is_weekend(code: int) -> bool:
    # 주말인지 체크하는 필터
    return {
        6: True,  # 일요일
        5: True,  # 토요일
    }.get(code, False)


def get_day_name(code: int) -> str:
    # 요일 이름 불러오는 필터
    return {
        6: "일",  # 주말
        0: "월",
        1: "화",
        2: "수",
        3: "목",
        4: "금",
        5: "토",  # 주말
    }.get(code)
