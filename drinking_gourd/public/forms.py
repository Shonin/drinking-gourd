# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import Form, RecaptchaField
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from drinking_gourd.user.models import User

class ForgotPassword(Form):
    """ User enters their email to request a password reset """
    email = StringField('Email Address', validators=[DataRequired("Pleaes enter your email"), Email("Enter a valid email")])
    recaptcha = RecaptchaField()
    submit = SubmitField("Reset Password")

class ResetPassword(Form):
    """ User enters a new password after requesting a reset """
    password = PasswordField('New password',
                             validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify new password',
                            [DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField("Reset Password")


class ContactForm(Form):
    """Contact Form"""

    name = StringField('Full Name', validators=[DataRequired("Please enter your name")])
    email = StringField('Email Address', validators=[DataRequired("Pleaes enter your email"), Email("Enter a valid email")])
    message = TextAreaField('Message', validators=[DataRequired("Please enter a message")])
    recaptcha = RecaptchaField()
    submit = SubmitField("Send")


class LoginForm(Form):
    """Login form."""

    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter(User.email.ilike(self.email.data)).first()
        
        if not self.user:
            self.email.errors.append('Unknown email')
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        if not self.user.active:
            self.username.errors.append('User not activated')
            return False
        return True
