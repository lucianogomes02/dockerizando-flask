from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

engine = create_engine("postgresql+psycopg2://test:test@localhost:5432/test", echo=True, future=True)
Base.metadata.create_all(engine)
