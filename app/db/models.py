from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import engine

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    active = Column(Boolean)


Base.metadata.create_all(bind=engine)
