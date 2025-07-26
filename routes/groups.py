from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Group, GroupMembership

groups_bp = Blueprint('groups', __name__, url_prefix='/groups')

@groups_bp.route('/')
@login_required
def list_groups():
    memberships = GroupMembership.query.filter_by(user_id=current_user.id).all()
    groups = [m.group for m in memberships]
    return render_template('groups/groups.html', groups=groups)

@groups_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_group():
    if request.method == 'POST':
        group = Group(
            name=request.form['name'],
            description=request.form['description'],
            creator_id=current_user.id
        )
        db.session.add(group)
        db.session.commit()
        membership = GroupMembership(group_id=group.id, user_id=current_user.id)
        db.session.add(membership)
        db.session.commit()
        flash("Group created!")
        return redirect(url_for('groups.list_groups'))
    return render_template('groups/create_group.html')

@groups_bp.route('/join/<int:group_id>', methods=['POST'])
@login_required
def join_group(group_id):
    membership = GroupMembership(group_id=group_id, user_id=current_user.id)
    db.session.add(membership)
    db.session.commit()
    flash("Joined group!")
    return redirect(url_for('groups.list_groups'))