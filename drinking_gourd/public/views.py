# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request
from flask import url_for, abort, session, jsonify
from flask_login import login_required, login_user, current_user

from drinking_gourd.extensions import login_manager, bcrypt
from drinking_gourd.public.forms import LoginForm, ContactForm, ForgotPassword, ResetPassword
from drinking_gourd.user.forms import RegisterForm
from drinking_gourd.user.models import User
from drinking_gourd.utils import flash_errors

from drinking_gourd.database import db

# Validate email and reset password tokens
from drinking_gourd.token import confirm_token

# Send password, confirmation, and contact emails
from drinking_gourd.send_emails import send_contact_email, send_password_reset_email

import feedparser
from flask.ext.paginate import Pagination

blueprint = Blueprint('public', __name__, static_folder='../static')


""" Might be able to delete this...?"""
@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Render the home page."""
    return render_template('public/index.html')

@blueprint.route('/about/')
def about():
    """Render the about page page."""
    return render_template('public/about.html')

@blueprint.route('/podcast/')
def podcast():
    """Render the podcasts page."""
    feed = feedparser.parse('http://thedrinkinggourd.org/rss')

    """PAGNATION"""
    search = False
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
    
    pagination = Pagination(page=page, total=len(feed.entries), search=search, record_name='podcasts',
        format_total=True,format_number=True)
    

    return render_template('public/podcast.html', page = page, feed = feed, pagination = pagination)

@blueprint.route('/contact-us/', methods=['GET', 'POST'])
def contact():
    """Contact Us page."""
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('public/contact.html', form = form)
        else:
            name = form.name.data
            email = form.email.data
            message = form.message.data
            send_contact_email(name, email, message)
            flash('Contact form submited. We will be in touch with you as soon as possible', 'success')
            return render_template('public/contact.html', form = form)
    return render_template('public/contact.html', form = form)


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        
        """Create User if form is valid"""
        User.create(email=form.email.data,
            full_name=form.full_name.data,
            password=form.password.data, 
            active=True)
        
        """Find user, login, send a confirm email, redirect to home with flashed message"""
        user = User.query.filter_by(email = form.email.data).first()
        login_user(user)
        flash('Thank you for registering.', 'success')
        return redirect(url_for('public.home'))

    else:
        """Send error message if form is not valid"""
        flash_errors(form)

    """Render html if not a POST request"""
    return render_template('public/register.html', form=form)

@blueprint.route('/login/', methods=['GET', 'POST'])
def login_page():
    """Login page."""
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            return redirect(url_for('public.home'))
        else:
            flash("We didn't recognize that, please try again", 'danger')
            return render_template('public/login.html', form=form)
    else:
        return render_template('public/login.html', form=form)


@blueprint.route('/forgot-password/', methods=['GET', 'POST'])
def forgotPassword():
    """Password page, user requests a password reset email"""
    form = ForgotPassword()
    if request.method == 'POST':
        if form.validate() == True:

            user = User.query.filter_by(email = form.email.data).first()
            
            # Alert user that the email wasn't found
            if not user:
                flash("We didn't find an account associated with that email :(", 'danger')
                return render_template('public/forgotpassword.html', form = form)

            send_password_reset_email(user)

            flash('Password reset. Please check your email', 'success')
            return redirect(url_for('public.home'))

        # Alert the user that the form was invalid
        else:
            flash('There was something wrong with the form, please try again', 'danger')
            return render_template('public/forgotpassword.html', form = form)
    
    # Render template for GET request
    else:
        return render_template('public/forgotpassword.html', form = form)



@blueprint.route('/password-reset/<token>/', methods=['GET', 'POST'])
def resetPassword(token):
    """Reset Password page, user resets password with confirm email"""
    try:
        email = confirm_token(token)
    except:
        return abort(404)

    form = ResetPassword()
    if request.method == 'POST':
        if form.validate() == True:
            user = db.session.query(User).filter_by(email = email).first()
            
            # get password from form and encrypt
            password = form.password.data
            password = bcrypt.generate_password_hash(password)

            #set new encrypted password to user
            user.password = password

            db.session.add(user)
            db.session.commit()

            flash('Password Reset', 'success')
            return redirect(url_for('public.login_page'))
        else:
            flash('Error, please try again', 'danger')
            return render_template('public/resetpassword.html', form = form, token=token)
    
    return render_template('public/resetpassword.html', form = form, token=token)