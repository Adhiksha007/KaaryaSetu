from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from extensions import db, mail
from db_models.user_auth import UserAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
import random

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm = request.form['confirm_password']

    if password != confirm:
        flash('Register Error: Passwords do not match.', 'danger')
        return redirect(url_for('job.home', open_modal='registerModal'))

    if UserAuth.query.filter((UserAuth.username == username) | (UserAuth.email == email)).first():
        flash('Register Error: Username or email already exists.', 'danger')
        return redirect(url_for('job.home', open_modal='registerModal'))

    hashed = generate_password_hash(password)
    new_user = UserAuth(username=username, email=email, password=hashed)
    db.session.add(new_user)
    db.session.commit()

    flash('Registration successful! You can now log in.', 'success')
    return redirect(url_for('job.home', open_modal='loginModal'))

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password_input = request.form['password']

    user = UserAuth.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password_input):
        session['user_id'] = user.id
        session['username'] = user.username
        flash('Login successful!', 'success')
        return redirect(url_for('job.home'))
    else:
        flash('Login Error: Invalid credentials.', 'danger')
        return redirect(url_for('job.home', open_modal='loginModal'))

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    email = request.form['email']
    user = UserAuth.query.filter_by(email=email).first()
    if not user:
        flash("Forgot Password Error: Email not found.", "danger")
        return redirect(url_for('job.home', open_modal="forgotPasswordModal"))

    otp = str(random.randint(100000, 999999))
    session['otp'] = otp
    session['reset_email'] = email

    msg = Message("Your OTP for Password Reset", recipients=[email])
    msg.body = f"Your OTP is: {otp}"
    mail.send(msg)

    flash("OTP has been sent to your email.", "info")
    return redirect(url_for('job.home', open_modal="resetPasswordModal"))

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    input_otp = request.form['otp']
    new_pw = request.form['new_password']
    confirm_pw = request.form['confirm_password']

    if input_otp != session.get('otp'):
        flash("Reset Error: Invalid OTP.", "danger")
        return redirect(url_for('job.home', open_modal='resetPasswordModal'))

    if new_pw != confirm_pw:
        flash("Reset Error: Passwords do not match.", "warning")
        return redirect(url_for('job.home', open_modal='resetPasswordModal'))

    email = session.get('reset_email')
    user = UserAuth.query.filter_by(email=email).first()
    if user:
        user.password = generate_password_hash(new_pw)
        db.session.commit()

    session.pop('otp', None)
    session.pop('reset_email', None)

    flash("Password reset successful. You can now log in.", "success")
    return redirect(url_for('job.home', open_modal='loginModal'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('job.home'))
