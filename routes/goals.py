from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Goal, Behavior

goals_bp = Blueprint('goals', __name__, url_prefix='/goals')

@goals_bp.route('/')
@login_required
def list_goals():
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    return render_template('goals/goals.html', goals=goals)

@goals_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_goal():
    behaviors = Behavior.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        goal = Goal(
            behavior_id=request.form['behavior_id'],
            target_count=request.form['target_count'],
            period=request.form['period'],
            user_id=current_user.id
        )
        db.session.add(goal)
        db.session.commit()
        flash("Goal added!")
        return redirect(url_for('goals.list_goals'))
    return render_template('add_goal.html', behaviors=behaviors)