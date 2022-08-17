from flask import Flask
from usuario.apis import usuario, spec

app = Flask(__name__)

app.register_blueprint(usuario)
spec.register(app)

if __name__ == "__main__":
    app.run()
