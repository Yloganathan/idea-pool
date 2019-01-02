import os

class Config:
    DEBUG = os.environ.get('DEBUG') or False
    DB_URI = os.environ.get('DB_URI')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') 
    JWT_BLACKLIST_ENABLED = os.environ.get('JWT_BLACKLIST_ENABLED') or True
    JWT_BLACKLIST_TOKEN_CHECKS =  ['access', 'refresh']
    JWT_TOKEN_LOCATION = ['headers', 'json']
    JWT_REFRESH_JSON_KEY = 'refresh_token'
    JWT_HEADER_NAME = 'x-access-token'
    JWT_HEADER_TYPE = ''
    PAGE_SIZE = 10

class DevelopmentConfig(Config):
    DEBUG = True
    DB_URI = 'idea-pool.db'
    JWT_SECRET_KEY = 'jwt-secret-string'
    

class TestConfig(Config):
    DEBUG = True
    TESTING = True
    DB_URI = 'idea-pool-test.db'
    JWT_SECRET_KEY = 'jwt-secret-string'

