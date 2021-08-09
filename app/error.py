
from flask import render_template


def bad_request(error):
    return render_template(
        "error/error.html",
        title="잘못된 요청",

        message="잘못된 요청입니다"
    ), getattr(error, "code")


def forbidden(error):
    return render_template(
        "error/error.html",
        title="잘못된 요청",

        message="접근할 수 없습니다"
    ), getattr(error, "code")


def page_not_found(error):
    return render_template(
        "error/error.html",
        title="페이지를 찾을 수 없음",

        message="해당 페이지를 찾을 수 없습니다"
    ), getattr(error, "code")


def method_not_allowed(error):
    return render_template(
        "error/error.html",
        title="잘못된 요청",

        message="해당 요청 방식은 사용할 수 없습니다"
    ), getattr(error, "code")


def internal_server_error(error):
    return render_template(
        "error/error.html",
        title="스크립트 오류 발생",

        message="내부 스크립트 오류가 발생하였습니다"
    ), getattr(error, "code")
