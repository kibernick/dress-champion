import logging

from flask import Flask
from flask_migrate import Migrate


log = logging.getLogger(__name__)


def create_app():
    app = Flask('dress_upi')
    from dress_champion.default_settings import DefaultSettings
    app.config.from_object(DefaultSettings)
    try:
        # In a real-world project would use `app.config.from_envvar('YOURAPPLICATION_SETTINGS')`
        app.config.from_pyfile('dress_champion/config.py')
    except FileNotFoundError as e:
        log.warning("File: `%s` not found, continuing with default settings" % e.filename)

    from dress_champion.models import db
    db.init_app(app)

    from dress_champion.schemas import ma
    ma.init_app(app)

    Migrate(app, db)

    return app
