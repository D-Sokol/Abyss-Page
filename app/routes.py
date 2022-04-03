from flask import Blueprint, render_template, request
from .services import get_counter, add_record

bp = Blueprint("main", __name__)


@bp.route("/")
@bp.route("/index")
def main():
    agent = request.user_agent
    params = request.query_string.decode()
    add_record(agent.string, params or None)
    n_items = get_counter()
    return render_template("main.html", n_items=n_items)
