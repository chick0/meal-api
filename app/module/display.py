# -*- coding: utf-8 -*-
from json import loads, dumps
from uuid import uuid4
from datetime import datetime, timedelta

from flask import session
from flask import render_template, redirect, url_for

from sqlalchemy.exc import OperationalError

from app.module.api import search_meal_by_codes
from app.module.cache import add_cache, get_cache_by_data


def return_meal(date: str or datetime, edu_code: str, school_code: str):
    if isinstance(date, datetime):
        # 오늘의 급식 메뉴 조회
        not_today = False
    else:
        # 사용자 지정 날짜 급식 메뉴 조회
        not_today = True
        try:
            # 날짜 형식 검사
            date = datetime.strptime(date, "%Y%m%d")
        except (ValueError, Exception):
            # 잘못된 날짜 형식
            session['alert'] = "지원하는 날짜 형식이 아닙니다"
            return redirect(url_for("index.index"))

    # DB에 저장된 캐시 검색
    try:
        result = get_cache_by_data(
            edu=edu_code,
            school=school_code,
            date=date.strftime('%Y%m%d')
        )
    except (OperationalError, Exception):  # DB 접속 실패
        result = None

    # DB 에서 발견된 캐시가 있나 검사
    if result is None:
        # 요청 경로에 포함된 교육청 코드와 학교 코드로 학교 검색
        try:
            meal, status_code = search_meal_by_codes(
                edu_code=edu_code,
                school_code=school_code,
                date=date.strftime('%Y%m%d')
            )
        except (ValueError, Exception):
            # 교육청 점검, 타임아웃 처리 단계
            session['alert'] = "급식 정보를 불러오는 데 실패했습니다"
            return redirect(url_for("index.index"))

        if status_code == 200:  # API 응답이 200인 경우
            try:
                # 데이터 분해하기
                result = meal['mealServiceDietInfo']

                # `row` 찾기
                for i in result:
                    for j in i.keys():
                        if j == "row":
                            result = i[j]
                            break
            except (KeyError, Exception):
                # 급식 정보 불러오기 실패
                return meal_data_not_found(
                    date=date,                # 날짜 정보
                    not_today=not_today,      # 오늘 메뉴인지 검사용

                    edu_code=edu_code,        # 교육청 코드
                    school_code=school_code   # 학교 코드
                )

            try:
                # DB 캐싱하기
                add_cache(
                    edu=edu_code,
                    school=school_code,
                    date=int(date.strftime('%Y%m%d')),
                    json=dumps(
                        obj=result
                    )
                )
            except (OperationalError, Exception):  # DB 접속 실패
                pass

        else:  # 에러 페이지로 보내기
            session['alert'] = "급식 정보를 불러오는 데 실패했습니다"
            return redirect(url_for("index.index"))

    else:  # 캐시가 있음
        result = loads(result.json)

    # 쿠키 저장용 세션 생성
    idx = None
    for s in session:  # 등록된 변수 확인
        try:
            # 교육청 코드 & 학교 코드 확인
            if session[s]['edu'] == edu_code and session[s]['school'] == school_code:
                # 구 세션 ID 사용
                idx = s
        except (KeyError, TypeError, Exception):
            pass

    if idx is None:  # 세션 재활용 실패
        # id 발급
        idx = str(uuid4())

    # 세션 정보 업데이트
    session[idx] = dict(
        edu=edu_code,
        school=school_code,
        name=result[0]['SCHUL_NM'],
        date=date.strftime('%Y%m%d')
    )

    # 급식 출력하기
    return show_meal(
        date=date,                        # 날짜 정보
        not_today=not_today,              # 오늘 메뉴인지 검사용

        edu_code=edu_code,                # 교육청 코드
        school_code=school_code,          # 학교 코드

        result=result,                    # 급식 정보

        idx=idx                           # 세션 정보
    )


def show_meal(date: datetime, not_today: bool, edu_code: str, school_code: str, result: list, idx: str):
    # 표기 날짜
    day = date.strftime('%Y년 %m월 %d일')

    # 내일 이동 버튼을 위한 값
    tomorrow = int((date + timedelta(days=1)).strftime('%Y%m%d'))

    # 어제 이동 버튼을 위한 값
    yesterday = int((date - timedelta(days=1)).strftime('%Y%m%d'))

    # 급식 표시하기
    return render_template(
        "meal/show.html",
        title=result[0]['SCHUL_NM'],  # 학교 이름
        use_modal=True,

        day=day,                      # ----년 --월 --일
        result=result,                # 급식 조회 결과

        edu_code=edu_code,            # 교육청 코드
        school_code=school_code,      # 학교 코드
        yesterday=yesterday,          # 어제
        tomorrow=tomorrow,            # 내일

        not_today=not_today,          # 오늘 메뉴인지 검사용
        idx=idx                       # 세션 정보
    )


def meal_data_not_found(date, not_today: bool, edu_code: str, school_code: str):
    # 표기 날짜
    day = date.strftime('%Y년 %m월 %d일')

    # 내일 이동 버튼을 위한 값
    tomorrow = int((date + timedelta(days=1)).strftime('%Y%m%d'))

    # 어제 이동 버튼을 위한 값
    yesterday = int((date - timedelta(days=1)).strftime('%Y%m%d'))

    # 급식 정보 불러오기 실패
    return render_template(
        "error/meal_data_not_found.html",
        title="정보 없음",
        use_modal=True,

        day=day,                      # ----년 --월 --일

        edu_code=edu_code,            # 교육청 코드
        school_code=school_code,      # 학교 코드
        yesterday=yesterday,          # 어제
        tomorrow=tomorrow,            # 내일

        not_today=not_today           # 오늘 메뉴인지 검사용
    )
