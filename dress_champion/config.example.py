import logging

DEBUG = True
TESTING = True

LOG_LEVEL = logging.DEBUG

SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost/database'
"""Main project database."""

TEST_DATABASE_URI = 'mysql://user:password@localhost/database_test'
"""A database that is setup and torn down when the tests are run."""
