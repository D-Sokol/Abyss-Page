from flask import Blueprint, abort, current_app, render_template, request
from functools import wraps
from http import HTTPStatus

from ..services import clear_all, get_counter, get_last_records

bp = Blueprint("admin", __name__, url_prefix="/admin")


def login_required(handler):
    @wraps(handler)
    def wrapper(*args, **kwargs):
        secret = request.values.get("secret")
        if not secret:
            abort(HTTPStatus.UNAUTHORIZED)
        elif secret != current_app.config["SECRET"]:
            abort(HTTPStatus.FORBIDDEN)
        return handler(*args, **kwargs)
    return wrapper


@bp.route("/")
@bp.route("/index")
@login_required
def main():
    n_items = get_counter()
    last_records = get_last_records(10)
    return render_template("admin.html", n_items=n_items, last_records=last_records)


@bp.route("/clear")
@login_required
def clear_database():
    items_removed = clear_all()
    return render_template("clear.html", items_removed=items_removed)