from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Reminder, Behavior

reminders_bp = Blueprint('reminders', __name__, url_prefix='/reminders')

@reminders_bp.route('/')
@login_required
def list_reminders():
    reminders = Reminder.query.filter_by(user_id=current_user.id).all()
    return render_template('reminders/reminders.html', reminders=reminders)

@reminders_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_reminder():
    behaviors = Behavior.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        reminder = Reminder(
            behavior_id=request.form['behavior_id'],
            time=request.form['time'],
            user_id=current_user.id
        )
        db.session.add(reminder)
        db.session.commit()
        flash("Reminder added!")
        return redirect(url_for('reminders.list_reminders'))
    return render_template('reminders/add_reminder.html', behaviors=behaviors)