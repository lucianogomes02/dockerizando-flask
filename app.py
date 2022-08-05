from flask import Flask, request, jsonify
from usuario import Usuario, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from datetime import datetime

app = Flask(__name__)

engine = create_engine("postgresql+psycopg2://test:test@postgresql/flask_api", echo=True, future=True)
Base.metadata.create_all(engine)


@app.route('/', methods=["GET"])
def bem_vindo():
    return {"ola": "bem-vindo!"}


@app.route('/usuario/cadastrar', methods=["POST"])
def cadastrar_usuario():
    if novo_usuario_eh_valido(dict(request.json)):
        novo_usuario = Usuario(
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
                return jsonify(
                    {
                        "sucesso": f"Usuario {novo_usuario.nome} cadastrado com sucesso!"
                    }
                )
    return jsonify(
        {
            "erro" : f"Nome de usuário inválido para cadastro. Verifique o body request!"
        }
    )


@app.route('/usuarios', methods=["GET"])
def pegar_usuarios():
    usuarios = list()
    with Session(bind=engine) as session:
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
