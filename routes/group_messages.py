from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, GroupMessage, GroupMembership

group_messages_bp = Blueprint('group_messages', __name__, url_prefix='/group-messages')

@group_messages_bp.route('/<int:group_id>')
@login_required
def messages(group_id):
    # Only members can view messages
    membership = GroupMembership.query.filter_by(user_id=current_user.id, group_id=group_id).first()
    if not membership:
        flash("You are not a member of this group.")
        return redirect(url_for('groups.list_groups'))
    messages = GroupMessage.query.filter_by(group_id=group_id).order_by(GroupMessage.timestamp.desc()).all()
    return render_template('groups/group_messages.html', messages=messages, group_id=group_id)

@group_messages_bp.route('/<int:group_id>/send', methods=['POST'])
@login_required
def send_message(group_id):
    membership = GroupMembership.query.filter_by(user_id=current_user.id, group_id=group_id).first()
    if not membership:
        flash("You are not a member of this group.")
        return redirect(url_for('groups.list_groups'))
    message = GroupMessage(
        group_id=group_id,
        sender_id=current_user.id,
        message=request.form['message']
    )
    db.session.add(message)
    db.session.commit()
    flash("Message sent!")
    return redirect(url_for('group_messages.messages', group_id=group_id))