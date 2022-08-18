from flask import Flask
from usuario.apis import usuario, spec
from usuario.migrations import usuario_migration
from .db import engine

app = Flask(__name__)

app.register_blueprint(usuario)
spec.register(app)

usuario_migration.create(engine, checkfirst=True)

if __name__ == "__main__":
    app.run(debug=True)
