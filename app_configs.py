# essa classe deve ter os campos limpos, pra não passar informações pro git

class Config(object):
    DB_HOST = "localhost"
    DB_NAME = "mogai"
    DB_USER = "postgres"
    DB_PASSWORD = ""
    DB_PORT = "5423"
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'chave_secreta'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ''
    JWT_SECRET_KEY = 'chave_secreta'

# Não sei se vai precisar dessas coisas ainda
class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True