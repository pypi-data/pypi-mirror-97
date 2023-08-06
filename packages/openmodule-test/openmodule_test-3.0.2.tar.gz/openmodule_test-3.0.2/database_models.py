import uuid

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DatabaseTestModel(Base):
    __tablename__ = "test"
    id = Column(String, default=lambda: str(uuid.uuid4()), unique=True, primary_key=True)
    value1 = Column(Integer, default=1)
    value2 = Column(Integer, default=2)
    string = Column(String, default="initial")
