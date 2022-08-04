from flask import Flask
from usuario import Usuario, Base
from sqlalchemy import create_engine

app = Flask(__name__)

engine = create_engine("postgresql+psycopg2://test:test@postgresql/test", echo=True, future=True)
Base.metadata.create_all(engine)


@app.route('/')
def ola_mundo():
    return {"ola": "mundo"}
