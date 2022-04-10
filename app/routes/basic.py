from flask import Blueprint, current_app, render_template, request, redirect

from ..services import get_counter, add_record
from ..feedback import send_feedback, FeedbackForm

bp = Blueprint("main", __name__)


@bp.route("/")
@bp.route("/index")
def webhook():
    return "OK"


@bp.route("/abyss")
def main():
    agent = request.user_agent
    params = request.query_string.decode()
    add_record(agent.string, params or None)
    n_items = get_counter()
    return render_template("main.html", n_items=n_items)


@bp.route("/achievement")
def achievement():
    return render_template("achievement.html")


@bp.route("/feedback", methods=["GET", "POST"])
def feedback():
    form = FeedbackForm()
    if form.is_submitted():
        message = form.message.data
        send_feedback(message)
        return redirect(current_app.config["UNIVERSAL_PAGE"])
    else:
        return render_template("feedback.html", form=form)
