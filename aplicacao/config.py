from os import urandom
from binascii import hexlify


class Configuracao(object):
    SECRET_KEY = hexlify(urandom(24))
    SQLALCHEMY_SERVER = "postgresql"

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"postgresql+psycopg2://test:test@{self.SQLALCHEMY_SERVER}:5432/test"


class ConfiguracaoProducao(Configuracao):
    DEBUG = False


class ConfiguracaoDesenvolvimento(Configuracao):
    DEBUG = True
    SQLALCHEMY_SERVER = "localhost"
