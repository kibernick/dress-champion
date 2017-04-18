import logging

from flask import Flask
from flask_migrate import Migrate

from dress_champion.utils import configure_logger


log = logging.getLogger(__name__)
configure_logger(log, logging.DEBUG)


def create_app(name='dress_champion', config_filename='config.py'):
    app = Flask(name)
    from dress_champion.default_settings import DefaultSettings
    app.config.from_object(DefaultSettings)
    try:
        # In a real-world project would use `app.config.from_envvar('YOURAPPLICATION_SETTINGS')`
        app.config.from_pyfile(config_filename)
    except FileNotFoundError as e:
        import pdb; pdb.set_trace()
        log.warning("File: `%s` not found, continuing with default settings" % e.filename)

    configure_logger(log, app.config['LOG_LEVEL'])

    from dress_champion.models import db
    db.init_app(app)

    from dress_champion.schemas import ma
    ma.init_app(app)

    Migrate(app, db)

    return app
