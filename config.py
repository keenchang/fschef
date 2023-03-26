import os 
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Default settings
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    # Settings applicable to all environments
    SECRET_KEY = os.getenv('SECRET_KEY', default='1234')

    # settings for folder of save images
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')

    # settings for Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("postgres", "postgresql")
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

    # Settings for AWS S3
    AMAZON_S3_ID = os.getenv('AMAZON_S3_ID')
    AMAZON_S3_KEY = os.getenv('AMAZON_S3_KEY')
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    S3_REGION = os.getenv('S3_REGION')
    
class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False

