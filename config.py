import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    SQLALCHEMY_ECHO = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
#     SQLALCHEMY_ECHO = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
