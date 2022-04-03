from flask import Blueprint, render_template

bp = Blueprint("main", __name__)


@bp.route("/")
@bp.route("/index")
def main():
    return render_template("main.html")
