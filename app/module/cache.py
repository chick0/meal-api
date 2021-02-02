# -*- coding: utf-8 -*-

from app import db
from app.module.cleaner import clean

from models import Meal


# 교육청 코드와 학교 코드와 날짜 정보로 캐시 불러오는 함수
def get_cache_by_data(edu: str, school: str, date: str):
    return Meal.query.filter_by(
        edu=edu,                # 교육청 코드
        school=school,          # 학교 코드
        date=date               # 날짜 정보
    ).first()


# 캐시 저장하는 함수
def add_cache(edu: str, school: str, date: int, json: str):
    json = clean(json_str=json)

    m = Meal(
        edu=edu,                # 교육청 코드
        school=school,          # 학교 코드
        date=date,              # 날짜 정보

        json=json               # 급식 정보
    )
    db.session.add(m)    # 급식 정보 DB 세션에 추가
    db.session.commit()  # 변경 사항 저장
