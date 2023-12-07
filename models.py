from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
