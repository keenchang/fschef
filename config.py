import os 
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Default settings
    FLASK_ENV = os.getenv('FLASK_ENV', default='development')
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    # Settings applicable to all environments
    SECRET_KEY = os.getenv('SECRET_KEY', default='1234')

    # settings for Database
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', default=False)

    # Setings for Session and Cookie
    SESSION_COOKIE_NAME = os.getenv('SESSION_COOKIE_NAME')
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)

    # Settings for Line Pay API
    CHANNEL_ID = os.getenv('CHANNEL_ID')
    CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')
    URL = os.getenv('URL')

    # Settings for 藍新金流 API
    MPG_MERCHANT_ID = os.getenv('MPG_MERCHANT_ID')
    MPG_IV = os.getenv('MPG_IV')
    MPG_KEY = os.getenv('MPG_KEY')
    
class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    FLASK_ENV = 'production'

