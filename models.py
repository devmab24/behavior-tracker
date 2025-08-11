from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    # Add relationships here if needed

class Behavior(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class LogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    behavior_id = db.Column(db.Integer, db.ForeignKey('behavior.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    note = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mood = db.Column(db.String(20))
    behavior = db.relationship('Behavior', backref='logs')


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    behavior_id = db.Column(db.Integer, db.ForeignKey('behavior.id'), nullable=False)
    target_count = db.Column(db.Integer, nullable=False)
    period = db.Column(db.String(20), default='week')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    behavior = db.relationship('Behavior', backref='goals')


class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    behavior_id = db.Column(db.Integer, db.ForeignKey('behavior.id'), nullable=False)
    time = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    behavior = db.relationship('Behavior', backref='reminders')


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(255))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class GroupMembership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    share_logs = db.Column(db.Boolean, default=True)
    share_goals = db.Column(db.Boolean, default=True)
    share_badges = db.Column(db.Boolean, default=True)
    group = db.relationship('Group', backref='memberships')

class GroupChallenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    challenge_text = db.Column(db.String(255))
    target_count = db.Column(db.Integer)
    period = db.Column(db.String(20))
    active = db.Column(db.Boolean, default=True)

class GroupMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sender = db.relationship('User', backref='sent_messages')
