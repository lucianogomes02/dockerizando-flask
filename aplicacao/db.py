from os import getenv
from flask import current_app

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, Session

engine = create_engine(current_app.config.get("SQLALCHEMY_DATABASE_URI"), echo=False, future=False)
metadata = MetaData(bind=engine)
Base = declarative_base(bind=engine)
session = Session(bind=engine, expire_on_commit=False)
