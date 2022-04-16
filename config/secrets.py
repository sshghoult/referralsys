from os import environ

SECRET_KEY = ''

POSTGRES_USER = environ.get('POSTGRES_USER', "postgres")
POSTGRES_PASSWORD = environ.get('POSTGRES_PASSWORD', "postgres")
POSTGRES_HOST = environ.get('POSTGRES_HOST', "localhost")
POSTGRES_PORT = environ.get('POSTGRES_PORT', 5432)
POSTGRES_DB = environ.get('POSTGRES_DB', "test")

REDIS_HOST = environ.get('REDIS_HOST',  "localhost")
REDIS_PORT = environ.get('REDIS_PORT', 5432)
DEBUG = environ.get('DEBUG', True)