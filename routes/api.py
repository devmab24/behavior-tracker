from flask import Blueprint, request, jsonify
from models import db, LogEntry as Log, Goal
from flask_login import login_required, current_user
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/logs', methods=['GET'])
@login_required
def list_logs():
    logs = Log.query.filter_by(user_id=current_user.id).order_by(Log.timestamp.desc()).limit(100).all()
    data = [{
        "id": l.id, "behavior_id": l.behavior_id, "note": l.note, "value": l.value, "timestamp": l.timestamp.isoformat()
    } for l in logs]
    return jsonify(data)

@api_bp.route('/logs', methods=['POST'])
@login_required
def create_log():
    payload = request.get_json() or {}
    behavior_id = payload.get('behavior_id')
    note = payload.get('note', '')
    value = int(payload.get('value', 1))
    if not behavior_id:
        return jsonify({"error":"behavior_id required"}), 400
    log = Log(behavior_id=behavior_id, user_id=current_user.id, note=note, value=value, timestamp=datetime.utcnow())
    db.session.add(log)
    db.session.commit()
    return jsonify({"success": True, "id": log.id}), 201

@api_bp.route('/goals', methods=['GET'])
@login_required
def list_goals():
    g = Goal.query.filter_by(user_id=current_user.id).all()
    return jsonify([{"id":x.id,"title":x.title,"target":x.target,"progress":x.progress} for x in g])

@api_bp.route('/goals', methods=['POST'])
@login_required
def create_goal():
    payload = request.get_json() or {}
    title = payload.get('title','Untitled')
    target = int(payload.get('target',0))
    goal = Goal(user_id=current_user.id, title=title, target=target, progress=0)
    db.session.add(goal)
    db.session.commit()
    return jsonify({"success":True,"id":goal.id}),201
