# -*- coding: utf-8 -*-
from random import randint

from app import db

from models import Poem


# 모든 시를 불러오는 함수
def get_all_ctx():
    return Poem.query.all()


# 저장된 시 목록 불러오는 함수
def get_list():
    titles = list()

    for ctx in get_all_ctx():
        titles.append(
            dict(
                author=ctx.author,
                title=ctx.title
            )
        )

    return titles


# 랜덤으로 시를 불러오는 함수
def get_random_ctx():
    ctx = get_all_ctx()
    if len(ctx) != 0:
        return ctx[randint(0, len(ctx) - 1)]
    else:
        return None


# 미리보기용 한 구절 불러오는 함수
def get_preview_from_ctx(ctx: Poem):
    # `\n`을 기준으로 줄 바꿈
    content = ctx.content.split("\n")

    # 작품에서 한 구절 랜점 추첨
    preview = content[randint(0, len(content) - 1)]

    if len(preview.strip()) != 0:  # 공백이 아닐 경우
        return preview
    else:                          # 공백이면 다시 추첨
        return get_preview_from_ctx(ctx=ctx)


# 시 ID 로 시 불러오는 함수
def get_ctx_by_poem_id(idx: int):
    return Poem.query.filter_by(
        idx=idx                 # 시 ID
    ).first()


# 시 작가와 제목으로 시 불러오는 함수
def get_ctx_by_metadata(author: str, title: str):
    return Poem.query.filter_by(
        author=author,          # 작가
        title=title             # 제목
    ).first()


# 시 추가하는 함수
def add_ctx(author: str, title: str, content: str):
    ctx = Poem(
        author=author,          # 작가
        title=title,            # 제목
        content=content,        # 본문
    )
    db.session.add(ctx)  # DB 세션에 추가
    db.session.commit()  # 변경 사항 저장


# 시 수정하는 함수
def edit_ctx(idx: int, author: str, title: str, content: str):
    ctx = get_ctx_by_poem_id(idx=idx)
    ctx.author = author
    ctx.title = title
    ctx.content = content

    db.session.commit()  # 변경 사항 저장


# 시 삭제하는 함수
def delete_ctx_by_id(idx: int):
    db.session.delete(get_ctx_by_poem_id(idx=idx))
    db.session.commit()
