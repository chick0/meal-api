# -*- coding: utf-8 -*-
from hashlib import sha512

from flask import Blueprint, request
from flask import render_template, redirect, url_for
from pyotp import TOTP

from app.module.poem import get_all_ctx, get_ctx_by_poem_id
from app.module.poem import add_ctx, edit_ctx, delete_ctx_by_id
from conf import conf


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


def auth():
    otp_token = conf['admin']['otp_token']
    password = conf['admin']['password']

    if sha512(request.form['password'].encode()).hexdigest() == password:
        if TOTP(otp_token).verify(otp=request.form['otp']):
            return True

    return False


@bp.route("/")
def index():
    ctx = get_all_ctx()
    ctx = sorted(ctx, key=lambda t: t.title)

    return render_template(
        "read_manage/index.html",
        title="시 관리 패널",

        context=ctx        # 작품들
    )


@bp.route("/add")
def add():
    return render_template(
        "read_manage/add.html",
        title="시 관리 패널"
    )


@bp.route("/adding", methods=["POST"])
def adding():
    if auth() is True:
        try:
            add_ctx(title=request.form['title'],
                    author=request.form['author'],
                    content=request.form['content'].replace("\r\n", "#"))
        except KeyError:
            pass

    return redirect(url_for("read_manage.index"))


@bp.route("/edit/<int:idx>")
def edit(idx: int):
    ctx = get_ctx_by_poem_id(idx=idx)
    if ctx is None:
        return redirect(url_for("read_manage.index"))

    author = ctx.author
    content = ctx.content.replace("#", "\r\n")

    return render_template(
        "read_manage/edit.html",
        idx=idx,           # 시 ID
        title=ctx.title,   # 제목
        author=author,     # 작가
        content=content    # 본문
    )


@bp.route("/editing/<int:idx>", methods=["POST"])
def editing(idx: int):
    if auth() is True:
        ctx = get_ctx_by_poem_id(idx=idx)
        if ctx is None:
            return redirect(url_for("read_manage.index"))

        try:
            edit_ctx(idx=idx,
                     title=request.form['title'],
                     author=request.form['author'],
                     content=request.form['content'].replace("\r\n", "#"))
        except KeyError:
            pass

    return redirect(url_for("read_manage.index"))


@bp.route("/delete/<int:idx>")
def delete(idx: int):
    ctx = get_ctx_by_poem_id(idx=idx)
    if ctx is None:
        return redirect(url_for("read_manage.index"))

    author = ctx.author
    content = ctx.content.replace("#", "\r\n")

    return render_template(
        "read_manage/delete.html",
        idx=idx,           # 시 ID
        title=ctx.title,   # 제목
        author=author,     # 작가
        content=content    # 본문
    )


@bp.route("/deleted/<int:idx>", methods=["POST"])
def deleted(idx: int):
    if auth() is True:
        ctx = get_ctx_by_poem_id(idx=idx)
        if ctx is None:
            return redirect(url_for("read_manage.index"))

        try:
            delete_ctx_by_id(idx=idx)
        except KeyError:
            pass

    return redirect(url_for("read_manage.index"))


@bp.route("/<int:idx>")
def show(idx: int):
    ctx = get_ctx_by_poem_id(idx=idx)
    if ctx is None:
        return redirect(url_for("read_manage.index"))

    return render_template(
        "read_manage/show.html",
        title=ctx.title,   # 제목

        idx=idx,           # 시 ID
        ctx=ctx            # 시 [제목, 작가, 본문]
    )
