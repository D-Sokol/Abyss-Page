import logging
import time
from flask import abort, Blueprint, current_app, render_template, request, redirect
from http import HTTPStatus
from ..services import get_counter, add_record, create_password
from ..feedback import send_feedback, FeedbackForm

bp = Blueprint("main", __name__)

feedback_password = create_password()
feedback_available_from = time.time()

logging.debug("Feedback password: %s", feedback_password)


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
    return render_template("achievement.html", password=feedback_password)


@bp.route("/feedback/<password>", methods=["GET", "POST"])
def feedback(password: str):
    global feedback_available_from
    global feedback_password
    now = time.time()
    if password != feedback_password or now < feedback_available_from:
        logging.info(
            "Feedback forbidden. Password: %s, time left: %f",
            password == feedback_password,
            max(0, feedback_available_from - now)
        )
        abort(HTTPStatus.NOT_FOUND)

    form = FeedbackForm()
    if form.is_submitted():
        message = form.message.data
        logging.info("Sending message: %s", message)
        send_feedback(message)
        feedback_password = create_password()
        feedback_available_from = time.time() + current_app.config["FEEDBACK_FREQ"]
        return redirect(current_app.config["UNIVERSAL_PAGE"])
    else:
        return render_template("feedback.html", form=form)
