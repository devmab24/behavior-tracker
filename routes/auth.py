from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('behaviors.list_behaviors'))
        flash('Invalid credentials')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'])
        user = User(username=request.form['username'], password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

from flask import current_app, send_from_directory, url_for
import os
from werkzeug.utils import secure_filename

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        display_name = request.form.get('display_name')
        avatar = request.files.get('avatar')
        if display_name:
            current_user.username = display_name
        if avatar and avatar.filename:
            filename = secure_filename(avatar.filename)
            uploads = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(uploads, exist_ok=True)
            path = os.path.join(uploads, filename)
            avatar.save(path)
            # You might want to persist avatar path in DB; for now attach to object
            current_user.avatar = url_for('static', filename='uploads/' + filename)
        db.session.commit()
        flash('Profile updated')
        return redirect(url_for('auth.profile'))
    return render_template('auth/profile.html')
