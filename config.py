import os
class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] #'sqlite:///posts.db'
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "dlmskfkjlemijfd"

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False

