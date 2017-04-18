import pytest

from dress_champion import create_app
from dress_champion.models import db as _db


CONFIG_FILENAME = 'dress_champion/config.py'


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application. Remember to set TEST_DATABASE_URI in your config file."""
    app = create_app('dress_champion_test', config_filename=CONFIG_FILENAME)
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': app.config['TEST_DATABASE_URI'],
    })

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


