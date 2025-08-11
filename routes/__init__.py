from .auth import auth_bp
from .behaviors import behaviors_bp
from .logs import logs_bp
from .goals import goals_bp
from .reminders import reminders_bp
from .groups import groups_bp
from .group_messages import group_messages_bp
from .group_challenges import group_challenges_bp
from .home import home_bp
from .api import api_bp


def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(behaviors_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(reminders_bp)
    app.register_blueprint(groups_bp)
    app.register_blueprint(group_messages_bp)
    app.register_blueprint(group_challenges_bp)