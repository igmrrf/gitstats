import os

from dotenv import load_dotenv
from flask import Flask

from .common.cache import cache
from .common.db import db
from .common.error import LibraryError, handle_library_error
from .common.limiter import limiter
from .common.login import login_manager
from .common.migrate import migrate
from .core import core_bp
from .auth import auth_bp
from .dashboard import dashboard_bp
from .insights import insights_bp

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///github_stats.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["GITHUB_CLIENT_ID"] = os.getenv("GITHUB_CLIENT_ID")
    app.config["GITHUB_CLIENT_SECRET"] = os.getenv("GITHUB_CLIENT_SECRET")
    app.config["CACHE_TYPE"] = "simple"
    app.config["RATELIMIT_DEFAULT"] = "100 per hour"

    # app.cli.add_command(init_db_commmand)

    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    app.register_blueprint(core_bp)
    app.register_blueprint(auth_bp, prefix_url="/auth")
    app.register_blueprint(dashboard_bp, prefix_url="/dashboard")
    app.register_blueprint(insights_bp, prefix_url="/insights")

    app.register_error_handler(LibraryError, handle_library_error)

    return app
