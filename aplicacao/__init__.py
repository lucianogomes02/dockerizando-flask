from dotenv import load_dotenv

load_dotenv()


def create_app(test_config=None):
    from flask import Flask

    app = Flask(__name__, instance_relative_config=True)

    with app.app_context():
        from .config import ConfiguracaoProducao, ConfiguracaoDesenvolvimento

        if app.config["ENV"] == "production":
            app.config.from_object(ConfiguracaoProducao())
        else:
            app.config.from_object(ConfiguracaoDesenvolvimento())

        from usuario.apis import usuario, spec
        from usuario.migrations import usuario_migration
        from .db import engine

        app.register_blueprint(usuario)
        spec.register(app)

        usuario_migration.create(engine, checkfirst=True)

    return app
