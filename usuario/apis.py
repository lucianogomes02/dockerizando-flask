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
    novo_usuario = UsuarioORM(
        nome=request.json.get("nome"),
        criado_em=datetime.now()
    )
    try:
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
    try:
        UsuarioRepoEscrita().atualizar(
            id_usuario=id_usuario,
            args=request.json
        )
    except Exception as erro:
        return jsonify(
            {
                "erro": f"Aconteceu um erro ao alterar o usuário {request.json.get('nome')}",
                "log": str(erro)
            }
        )
    else:
        return jsonify(
            Usuario(
                nome=request.json.get("nome"),
            ).dict()
        )


@usuario.delete('/<int:id_usuario>')
@spec.validate(resp=Response('HTTP_204'))
def deletar_usuario(id_usuario):
    try:
        UsuarioRepoEscrita().deletar(id_usuario=id_usuario)
    except Exception as erro:
        return jsonify(
            {
                "erro": f"Aconteceu um erro ao deletar o usuário",
                "log": str(erro)
            }
        )
    else:
        return jsonify({})
