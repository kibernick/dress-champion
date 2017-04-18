import logging


class DefaultSettings:
    DEBUG = False
    TESTING = False
    LOG_LEVEL = logging.WARNING

    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'
    TEST_DATABASE_URI = 'sqlite://:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    KAFKA_HOST_PORT = 'localhost:9092'
