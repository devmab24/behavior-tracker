from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Behavior

behaviors_bp = Blueprint('behaviors', __name__, url_prefix='/behaviors')

@behaviors_bp.route('/')
@login_required
def list_behaviors():
    behaviors = Behavior.query.filter_by(user_id=current_user.id).all()
    return render_template('behaviors/behaviors.html', behaviors=behaviors)

@behaviors_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_behavior():
    if request.method == 'POST':
        behavior = Behavior(
            name=request.form['name'],
            description=request.form['description'],
            user_id=current_user.id
        )
        db.session.add(behavior)
        db.session.commit()
        flash("Behavior added!")
        return redirect(url_for('behaviors.list_behaviors'))
    return render_template('edit_behavior.html')

@behaviors_bp.route('/edit/<int:behavior_id>', methods=['GET', 'POST'])
@login_required
def edit_behavior(behavior_id):
    behavior = Behavior.query.get_or_404(behavior_id)
    if request.method == 'POST':
        behavior.name = request.form['name']
        behavior.description = request.form['description']
        db.session.commit()
        flash("Behavior updated!")
        return redirect(url_for('behaviors.list_behaviors'))
    return render_template('edit_behavior.html', behavior=behavior)

@behaviors_bp.route('/delete/<int:behavior_id>', methods=['POST'])
@login_required
def delete_behavior(behavior_id):
    behavior = Behavior.query.get_or_404(behavior_id)
    db.session.delete(behavior)
    db.session.commit()
    flash("Behavior deleted!")
    return redirect(url_for('behaviors.list_behaviors'))