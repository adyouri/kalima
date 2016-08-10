import os
class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "dlmskfkjlemijfd"
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] #'sqlite:///posts.db'

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

