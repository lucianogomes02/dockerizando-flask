from flask import Flask, request, jsonify, redirect, url_for
from usuario import UsuarioORM, Base
from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import Session

from flask_pydantic_spec import FlaskPydanticSpec, Request, Response
from pydantic import BaseModel

from datetime import datetime
from typing import Optional, List

app = Flask(__name__)
spec = FlaskPydanticSpec("flask", title="Dockerizando Flask API")
spec.register(app)

engine = create_engine("postgresql+psycopg2://test:test@localhost:5432/test", echo=True, future=True)
Base.metadata.create_all(engine)


class Usuario(BaseModel):
    id: Optional[int]
    nome: str
    criado_em: Optional[str]


class Usuarios(BaseModel):
    usuarios: List[Usuario]


@app.get('/')
def api_doc():
    return redirect(url_for("doc_page_swagger"))


@app.post('/usuario/cadastrar')
@spec.validate(
    body=Request(Usuario),
    resp=Response(HTTP_200=Usuario)
)
def cadastrar_usuario():
    novo_usuario = UsuarioORM(
        nome=request.json.get("nome"),
        criado_em=datetime.now()
    )
    with Session(bind=engine, expire_on_commit=False) as session:
        session.begin()
        try:
            session.add(novo_usuario)
        except Exception:
            session.rollback()
        else:
            session.commit()
            session.close()
            return novo_usuario.para_dicionario()

# AJUSTAR VALIDAÇÃO DO PYDANTIC -- pydantic.errors.DictError: value is not a valid dict
@app.get('/usuarios')
@spec.validate(resp=Response(HTTP_200=Usuarios))
def pegar_usuarios():
    usuarios = list()
    with Session(bind=engine) as session:
        resultados = session.query(UsuarioORM).all()
        for usuario in resultados:
            usuarios.append(
                {
                    "id": usuario.id,
                    "nome": usuario.nome,
                    "criado_em": usuario.criado_em
                }
            )
        session.close()
    return jsonify(usuarios)

