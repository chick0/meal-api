# -*- coding: utf-8 -*-
from json import loads
from datetime import datetime

from flask import Blueprint
from flask import redirect, url_for, render_template

from app.module.cache import get_all_cache, get_cache_by_cache_id

bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


@bp.route("/")
def status():
    caches = get_all_cache()
    return render_template(
        "cache/status.html",
        title="캐시 관리 패널",

        count=len(caches),
        caches=caches
    )


@bp.route("/<int:idx>")
def get(idx: int):
    cache = get_cache_by_cache_id(idx=idx)

    if cache is None:
        return redirect(url_for(".status"))

    day = datetime.strptime(cache.date, "%Y%m%d").strftime('%Y년 %m월 %d일')

    result = loads(cache.json)

    # 급식 표시하기
    return render_template(
        "cache/show.html",
        title=result[0]['SCHUL_NM'],  # 학교 이름
        use_modal=True,

        day=day,                      # ----년 --월 --일
        result=result,                # 급식 조회 결과

        edu_code=cache.edu,           # 교육청 코드
        school_code=cache.school,     # 학교 코드

        idx=idx                       # 캐시 정보
    )
