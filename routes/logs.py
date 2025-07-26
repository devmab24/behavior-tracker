from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, LogEntry, Behavior

logs_bp = Blueprint('logs', __name__, url_prefix='/logs')

@logs_bp.route('/')
@login_required
def list_logs():
    logs = LogEntry.query.filter_by(user_id=current_user.id).order_by(LogEntry.timestamp.desc()).all()
    return render_template('logs/logs.html', logs=logs)

@logs_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_log():
    behaviors = Behavior.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        log = LogEntry(
            behavior_id=request.form['behavior_id'],
            note=request.form['note'],
            mood=request.form['mood'],
            user_id=current_user.id
        )
        db.session.add(log)
        db.session.commit()
        flash("Log added!")
        return redirect(url_for('logs.list_logs'))
    return render_template('logs/add_log.html', behaviors=behaviors)