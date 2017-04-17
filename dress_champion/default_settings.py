class DefaultSettings:
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    KAFKA_HOST_PORT = 'localhost:9092'
