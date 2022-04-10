from flask import current_app
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField


class FeedbackForm(FlaskForm):
    message = TextAreaField("Message")
    submit = SubmitField("Send")


mail = Mail()


def send_feedback(message: str):
    mail_username = current_app.config["MAIL_USERNAME"]
    msg = Message(
        "Message from feedback form",
        sender=mail_username,
        recipients=[mail_username],
        body=message,
    )
    mail.send(msg)
