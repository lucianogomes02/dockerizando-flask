from usuario.orm import Base
from sqlalchemy import create_engine

from pydantic import BaseModel

from datetime import datetime
from typing import Optional, List, Union


engine = create_engine("postgresql+psycopg2://test:test@localhost:5432/test", echo=True, future=True)
Base.metadata.create_all(engine)


class Usuario(BaseModel):
    id: Optional[int]
    nome: str
    criado_em: Optional[Union[datetime, str]]


class Usuarios(BaseModel):
    usuarios: List[Usuario]
