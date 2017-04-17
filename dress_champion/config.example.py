class DefaultSettings:
    DEBUG = True
    TESTING = True
    # examples:
    # sqlite:////tmp/test.db
    # mysql://username:password@server/db
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://scott:tiger@localhost/mydatabase'
