# -*- coding: utf-8 -*-
from json import dumps
from random import choice

from flask import Blueprint
from flask import request, session
from flask import render_template, Response
from flask import redirect, url_for

import read


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


@bp.route("/get")
def get():
    # 등록된 시 중에서 한 가지 추출
    ctx = getattr(read, choice(read.__all__))

    # 작품에서 한 구절 랜점 추첨
    preview = choice([text for text in ctx.CONTENT if len(text) != 0]).replace("&nbsp;", "")

    # 급식 세션 아이디 가져오기
    idx = request.args.get("idx", "none")

    # 해당 세션 아이디가 규칙을 따르는지 검사 ( s로 시작하는가 , 5자 인가 )
    if not idx.startswith("s") or len(idx) != 5:
        idx = None

    return Response(
        status=200,
        mimetype="application/json",
        response=dumps({
            "url": url_for("read.show", author=ctx.AUTHOR, title=ctx.TITLE, idx=idx),
            "preview": preview
        })
    )


@bp.route("")
def index():
    # 시 목록 불러오고, 제목순으로 정렬
    context = sorted([getattr(read, _id) for _id in read.__all__], key=lambda r: r.TITLE)

    # 급식 조회중인 학교 세션 아이디로 정보 불러오기
    idx = request.args.get("idx", "none")

    # 해당 세션 아이디가 규칙을 따르는지 검사 ( s로 시작하는가 , 5자 인가 )
    if idx.startswith("s") and len(idx) == 5 and idx in session.keys():
        button = session[idx]['name']
        target = url_for("meal.show",
                         edu_code=session[idx]['edu'],        # 교육청 코드
                         school_code=session[idx]['school'],  # 학교 코드
                         date=session[idx]['date'])           # 날짜 정보
    else:
        button = "학교 검색하러 가기"
        target = url_for("index.index")
        idx = None

    return render_template(
        "read/index.html",
        title="시",

        context=context,   # 작품들

        idx=idx,           # 세션 ID
        button=button,     # 뒤로가기 버튼 텍스트
        target=target      # 뒤로가기 버튼 목적지
    )


@bp.route("/<string:author>/<string:title>")
def show(author: str, title: str):
    try:
        # 작품 검색
        ctx = [ctx for ctx in [getattr(read, _id) for _id in read.__all__]
               if ctx.AUTHOR == author and ctx.TITLE == title][0]
    except IndexError:
        session['alert'] = "등록된 작품이 아닙니다"
        return redirect(url_for("index.index"))

    # 급식 조회중인 학교 세션 아이디로 정보 불러오기
    idx = request.args.get("idx", "none")

    # 해당 세션 아이디가 규칙을 따르는지 검사 ( s로 시작하는가 , 5자 인가 )
    if idx.startswith("s") and len(idx) == 5 and idx in session.keys():
        button = session[idx]['name']
        target = url_for("meal.show",
                         edu_code=session[idx]['edu'],        # 교육청 코드
                         school_code=session[idx]['school'],  # 학교 코드
                         date=session[idx]['date'])           # 날짜 정보
    else:
        button = "학교 검색하러 가기"
        target = url_for("index.index")
        idx = None

    return render_template(
        "read/show.html",
        title=ctx.TITLE,   # 제목

        ctx=ctx,           # 시 [제목, 작가, 본문]

        idx=idx,           # 세션 ID
        button=button,     # 뒤로가기 버튼 텍스트
        target=target      # 뒤로가기 버튼 목적지
    )


@bp.route("/random")
def random():
    # 등록된 시 중에서 한 가지 추출
    ctx = getattr(read, choice(read.__all__))

    return render_template(
        "read/random.html",
        title=ctx.TITLE,
        ctx=ctx
    )
