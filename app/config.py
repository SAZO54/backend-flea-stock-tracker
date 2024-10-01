import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://myuser:mypassword@localhost/flea_stock_tracker_test')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://myuser:mypassword@localhost/flea_stock_tracker_prod')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
