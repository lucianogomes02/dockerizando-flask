from sqlalchemy import Table, Column, Integer, String, DateTime
from aplicacao.db import metadata

usuario_migration = Table(
    "usuario",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nome", String(30), unique=False, nullable=False),
    Column("criado_em", DateTime(timezone=True), unique=False, nullable=False),
)
