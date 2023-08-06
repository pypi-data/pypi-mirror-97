from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import UniqueConstraint


engine = create_engine('sqlite:///score.db', echo=True)

Base = declarative_base()


class Configuration(Base):
    __table__ = "configuration"

    id = Column(Integer, primary_key=True)
    git_hash = Column(String, primary_key=True)
    git_hash_short = Column(String, primary_key=True)
    instance_str = Column(String, primary_key=True)

    UniqueConstraint('')

