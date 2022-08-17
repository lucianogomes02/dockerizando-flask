from pydantic import BaseModel

from datetime import datetime
from typing import Optional, List, Union


class Usuario(BaseModel):
    id: Optional[int]
    nome: str
    criado_em: Optional[Union[datetime, str]]


class Usuarios(BaseModel):
    usuarios: List[Usuario]
