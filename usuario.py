from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(30), unique=False, nullable=False)
    criado_em = Column(DateTime, unique=False, nullable=False)

    def __repr__(self):
        return f"<Usuario: {self.nome}>"
