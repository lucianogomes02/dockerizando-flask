from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

engine = create_engine("postgresql+psycopg2://test:test@localhost:5432/test", echo=True, future=True)
session = Session(bind=engine, expire_on_commit=False)

Base.metadata.create_all(engine)
