from flask import Blueprint
from flask import current_app
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import render_template

bp = Blueprint(
    name="poem",
    import_name="poem",
    url_prefix="/poem"
)


@bp.get("/<string:poem_id>")
def view(poem_id: str):
    edu = request.args.get("e", "")
    school = request.args.get("s", "")

    if len(edu) == 0 or len(school) == 0:
        back = url_for("index.index")
    else:
        back = url_for("meal.show", edu_code=edu, school_code=school)

    try:
        poem = current_app.config.get("poems", {})[poem_id]
    except KeyError:
        session['alert'] = "등록된 시가 아닙니다."
        return redirect(back)

    return render_template(
        "poem/view.html",
        title=f"{poem['author']} - {poem['title']}",
        poem=poem,
        back=back
    )
