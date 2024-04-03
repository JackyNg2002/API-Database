import os
from datetime import timedelta

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLITE3_DATABASE_PATH = os.getenv('SQLITE3_DATABASE_PATH')
    DATA_STORAGE_PATH = os.getenv('DATA_STORAGE_PATH')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{SQLITE3_DATABASE_PATH}'
    SQLALCHEMY_ECHO = True

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_BLOCKLIST_TOKEN_CHECKS = ['access']

    HOST_URL = os.getenv('HOST_URL')


class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI=f'sqlite:///../data/database/database.db'

class TestingConfig(Config):
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
