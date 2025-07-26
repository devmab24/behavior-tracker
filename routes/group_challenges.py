from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, GroupChallenge, GroupMembership

group_challenges_bp = Blueprint('group_challenges', __name__, url_prefix='/group-challenges')

@group_challenges_bp.route('/<int:group_id>')
@login_required
def list_challenges(group_id):
    membership = GroupMembership.query.filter_by(user_id=current_user.id, group_id=group_id).first()
    if not membership:
        flash("You are not a member of this group.")
        return redirect(url_for('groups.list_groups'))
    challenges = GroupChallenge.query.filter_by(group_id=group_id).all()
    return render_template('groups/group_challenges.html', challenges=challenges, group_id=group_id)

@group_challenges_bp.route('/<int:group_id>/add', methods=['GET', 'POST'])
@login_required
def add_challenge(group_id):
    membership = GroupMembership.query.filter_by(user_id=current_user.id, group_id=group_id).first()
    if not membership:
        flash("You are not a member of this group.")
        return redirect(url_for('groups.list_groups'))
    if request.method == 'POST':
        challenge = GroupChallenge(
            group_id=group_id,
            challenge_text=request.form['challenge_text'],
            target_count=request.form['target_count'],
            period=request.form['period'],
            active=True
        )
        db.session.add(challenge)
        db.session.commit()
        flash("Challenge added!")
        return redirect(url_for('group_challenges.list_challenges', group_id=group_id))
    return render_template('groups/add_challenge.html', group_id=group_id)