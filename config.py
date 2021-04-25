"""Flask configuration."""
from os import environ
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

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
    