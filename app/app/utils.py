from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import app, mail

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])


def send_email(email, subject, html):
    msg = Message(
        subject,
        recipients=[email],
        html=html,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
