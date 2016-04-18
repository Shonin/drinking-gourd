# Send emails

from flask import render_template, url_for
from drinking_gourd.mail import send_email
from drinking_gourd.token import generate_confirmation_token

def send_contact_email(name, email, message):
	"""Sends an email to an admin with a users message"""
	html = "New Message From: " + name + "<br>"
	html += "Email: " + email + "<br>"
	html += "Message: " + message 
	subject = "Your Contact Form"
	send_email('#@#.com', subject, html)

def send_password_reset_email(user):
	"""Sends an email to a user with a unique token
	that allows them to reset their password"""
	token = generate_confirmation_token(user.email)
	recover_url = url_for('public.resetPassword', token = token, _external = True)
	html = render_template('email/password.html', user=user, recover_url=recover_url)
	subject = "Password Reset Requested"
	send_email(user.email, subject, html)