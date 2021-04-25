"""Flask configuration."""
from os import environ
from dotenv import load_dotenv

load_dotenv('.env')

class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY')

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    
class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    