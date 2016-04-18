# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user 
from drinking_gourd.database import db

blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')

# =================================
# 			USER ROUTES
# =================================

@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))

@blueprint.route('/')
@login_required
def account():
	"""Show User Account Page."""
	return render_template('users/account.html')

@blueprint.route('/re-confirm/', methods = ['POST'])
@login_required
def reconfirmEmail():
    """Send user another confirm email if they didn't get the first"""
    user = current_user
    send_confirm_email(user)
    flash('Thank you, please check your email.', 'success')
    return redirect(url_for('public.home'))