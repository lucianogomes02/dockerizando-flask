from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UsuarioORM(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(30), unique=False, nullable=False)
    criado_em = Column(DateTime, unique=False, nullable=False)

    def __repr__(self):
        return f"<Usuario: {self.nome}>"

    def para_dicionario(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "criado_em": self.criado_em
        }
