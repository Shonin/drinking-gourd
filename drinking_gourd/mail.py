# send email functionality

from flask import current_app
from flask.ext.mail import Message
from drinking_gourd.extensions import mail

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config.get('MAIL_DEFAULT_SENDER')
    )
    mail.send(msg)