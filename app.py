from flask import Flask, request, jsonify
from usuario import Usuario, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

engine = create_engine("postgresql+psycopg2://test:test@postgresql/test", echo=True, future=True)
Base.metadata.create_all(engine)


@app.route('/', methods=["GET"])
def ola_mundo():
    return {"ola": "mundo"}


@app.route('/usuario/cadastro', methods=["POST"])
def cadastrar_usuario():
    if novo_usuario_eh_valido(dict(request.json)):
        novo_usuario = Usuario(
            nome=request.json.get("nome"),
            criado_em=datetime.now()
        )
        with Session(engine) as session:
            try:
                session.add(novo_usuario)
                session.commit()
                session.close()
                return jsonify(
                    {
                        "sucesso": f"Usuario cadastrado com sucesso!"
                    }
                )
            except Exception:
                session.rollback()
    return jsonify(
        {
            "erro" : f"Nome de usuário inválido para cadastro. Verifique o body request!"
        }
    )


@app.route('/usuarios', methods=["GET"])
def pegar_usuarios():
    usuarios = list()
    with Session(engine) as session:
        resultados = session.query(Usuario).all()
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


def novo_usuario_eh_valido(novo_usuario: dict):
    if "nome" in novo_usuario.keys() and novo_usuario.get("nome", ""):
        return True
    return False
