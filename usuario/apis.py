from .modelos import Usuario, Usuarios
from aplicacao.db import engine

from flask import request, jsonify, Blueprint
from flask_pydantic_spec import FlaskPydanticSpec
from .orm import UsuarioORM
from sqlalchemy.orm import Session

from flask_pydantic_spec import Request, Response

from datetime import datetime

from .repo import UsuarioRepoLeitura, UsuarioRepoEscrita

usuario = Blueprint("usuario", __name__, url_prefix="/usuario")
spec = FlaskPydanticSpec("flask", title="Dockerizando Flask API")


@usuario.get('/')
@spec.validate(resp=Response(HTTP_200=Usuarios))
def pegar_usuarios():
    usuarios = UsuarioRepoLeitura().buscar()
    return jsonify(
        Usuarios(
            usuarios=usuarios,
        ).dict()
    )


@usuario.post('/cadastrar')
@spec.validate(
    body=Request(Usuario),
    resp=Response(HTTP_201=Usuario)
)
def cadastrar_usuario():
    try:
        novo_usuario = UsuarioORM(
            nome=request.json.get("nome"),
            criado_em=datetime.now()
        )
        UsuarioRepoEscrita().adicionar(usuario=novo_usuario)
    except Exception as erro:
        return jsonify(
            {
                "erro": f"Aconteceu um erro ao cadastrar o usuário {novo_usuario.nome}",
                "log": str(erro)
            }
        )
    else:
        return jsonify(
            Usuario(
                id=novo_usuario.id,
                nome=novo_usuario.nome,
                criado_em=novo_usuario.criado_em
            ).dict()
        )


@usuario.put('/<int:id_usuario>')
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


@usuario.delete('/<int:id_usuario>')
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