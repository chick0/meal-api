# -*- coding: utf-8 -*-

from app import db


class Meal(db.Model):
    idx = db.Column(       # 캐시 ID (등록순서)
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    edu = db.Column(       # 교육청 코드
        db.String(8),
        nullable=False
    )
    school = db.Column(    # 학교 코드
        db.String(8),
        nullable=False
    )
    date = db.Column(      # 급식 날짜
        db.String(10),
        nullable=False
    )

    json = db.Column(      # 급식 정보
        db.Text,
        nullable=False
    )

    def __init__(self, edu, school, date, json):
        self.edu = edu
        self.school = school
        self.date = date

        self.json = json

    def __repr__(self):
        return f"<Meal idx={self.idx}>"


class Poem(db.Model):
    idx = db.Column(       # 시 ID (등록순서)
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    author = db.Column(    # 작가
        db.String(8),
        nullable=False
    )
    title = db.Column(     # 제목
        db.String(8),
        nullable=False
    )
    content = db.Column(   # 본문
        db.Text,
        nullable=False
    )

    def __init__(self, author, title, content):
        self.author = author
        self.title = title
        self.content = content

    def __repr__(self):
        return f"<Poem idx={self.idx}>"
