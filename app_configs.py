# essa classe deve ter os campos limpos, pra não passar informações pro git

class Config(object):
    DB_HOST = ""
    DB_NAME = ""
    DB_USER = ""
    DB_PASSWORD = ""
    DB_PORT = ""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ''

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