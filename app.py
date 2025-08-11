import os
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO
from models import db, User
from routes import register_blueprints

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev-secret-key")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///behavior.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Security / cookies settings (for production override with env vars)
    app.config['SESSION_COOKIE_SECURE'] = os.environ.get("SESSION_COOKIE_SECURE", "False") == "True"
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # init extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    csrf = CSRFProtect(app)
    # limiter = Limiter(app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])  
    limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])
    limiter.init_app(app)


    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    socketio = SocketIO(cors_allowed_origins="*")
    socketio.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    register_blueprints(app)

    @app.route("/health")
    def health():
        return {"status":"ok"}

    return app, socketio

app, socketio = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0")