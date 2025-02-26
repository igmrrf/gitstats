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
from .common.const import (
    github_client_id,
    secret_key,
    github_client_secret,
    ratelimit_default,
    sqalchemy_database_uri,
    sqalchemy_track_notifications,
    cache_type,
    postgres_url,
)

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config[secret_key] = os.getenv(secret_key)
    app.config[sqalchemy_database_uri] = os.getenv(postgres_url)
    app.config[sqalchemy_track_notifications] = False
    app.config[github_client_id] = os.getenv(github_client_id)
    app.config[github_client_secret] = os.getenv(github_client_secret)
    app.config[cache_type] = "simple"
    app.config[ratelimit_default] = "100 per hour"

    # app.cli.add_command(init_db_commmand)

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
