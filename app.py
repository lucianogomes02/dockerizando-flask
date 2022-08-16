from flask import Flask, request, jsonify, redirect, url_for
from usuario import UsuarioORM, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from flask_pydantic_spec import FlaskPydanticSpec, Request, Response
from pydantic import BaseModel

from datetime import datetime
from typing import Optional, List, Union

app = Flask(__name__)
spec = FlaskPydanticSpec("flask", title="Dockerizando Flask API")
spec.register(app)

engine = create_engine("postgresql+psycopg2://test:test@localhost:5432/test", echo=True, future=True)
Base.metadata.create_all(engine)


class Usuario(BaseModel):
    id: Optional[int]
    nome: str
    criado_em: Optional[Union[datetime, str]]


class Usuarios(BaseModel):
    usuarios: List[Usuario]


@app.get('/')
def api_doc():
    return redirect(url_for("doc_page_swagger"))


@app.get('/usuarios')
@spec.validate(resp=Response(HTTP_200=Usuarios))
def pegar_usuarios():
    usuarios = list()
    with Session(bind=engine) as session:
        resultados = session.query(UsuarioORM).all()
        for usuario in resultados:
            usuarios.append(usuario.para_dicionario())
        session.close()
    return jsonify(
        Usuarios(
            usuarios=usuarios,
        ).dict()
    )


@app.post('/usuario/cadastrar')
@spec.validate(
    body=Request(Usuario),
    resp=Response(HTTP_201=Usuario)
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
        except Exception as erro:
            session.rollback()
            return jsonify(
                {
                    "erro": f"Aconteceu um erro ao cadastrar o usuário {novo_usuario.nome}",
                    "log": str(erro)
                }
            )
        else:
            session.commit()
            session.close()
            return jsonify(
                Usuario(
                    id=novo_usuario.id,
                    nome=novo_usuario.nome,
                    criado_em=novo_usuario.criado_em
                ).dict()
            )


@app.put('/usuario/<int:id_usuario>')
@spec.validate(
    body=Request(Usuario),
    resp=Response(HTTP_201=Usuario, HTTP_500=None)
)
def alterar_usuario(id_usuario):
    with Session(bind=engine, autoflush=False) as session:
        try:
            body = request.json
            usuario = session.query(UsuarioORM).filter_by(id=id_usuario)
            if usuario:
                usuario.update({"nome": body.get("nome")})
        except Exception as erro:
            session.rollback()
            return jsonify(
                {
                    "erro": f"Aconteceu um erro ao alterar o usuário {body.get('nome')}",
                    "log": str(erro)
                }
            )
        else:
            session.commit()
            session.close()
            return jsonify(
                Usuario(
                    nome=body.get("nome"),
                ).dict()
            )


@app.delete('/usuario/<int:id_usuario>')
@spec.validate(resp=Response('HTTP_204'))
def deletar_usuario(id_usuario):
    with Session(bind=engine, autoflush=False) as session:
        try:
            usuario = session.query(UsuarioORM).filter_by(id=id_usuario).one()
            session.delete(usuario)
        except Exception as erro:
            session.rollback()
            return jsonify(
                {
                    "erro": f"Aconteceu um erro ao deletar o usuário",
                    "log": str(erro)
                }
            )
        else:
            session.commit()
    return jsonify({})


if __name__ == "__main__":
    app.run()
