import uuid
from typing import Type
import config
from cachetools import cached
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import EmailType, UUIDType
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

Base = declarative_base()


class User(Base):

    __tablename__ = "ads_users"

    id = Column(Integer, primary_key=True)
    email = Column(EmailType, unique=True, index=True)
    password = Column(String(60), nullable=False)
    registration_time = Column(DateTime, server_default=func.now())


class Token(Base):

    __tablename__ = "tokens"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    creation_time = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("ads_users.id", ondelete="CASCADE"))
    user = relationship("User", lazy="joined")


class Advertisments(Base):

    __tablename__ = "ads"

    id = Column(Integer, primary_key=True)
    header = Column(String(100), nullable=False)
    description = Column(String(300), nullable=False)
    date_of_creation = Column(DateTime, server_default=func.now())
    owner = Column(Integer, ForeignKey("ads_users.id", ondelete="CASCADE"))
    user = relationship("User", lazy="joined")


@cached({})
def get_engine():
    return create_async_engine(config.PG_DSN)


@cached({})
def get_session_maker():
    return sessionmaker(bind=get_engine(), expire_on_commit=False, class_=AsyncSession)


def init_db():
    Base.metadata.create_all(bind=get_engine())


def close_db():
    get_engine().dispose()


ORM_MODEL_CLS = Type[User] | Type[Token] | Type[Advertisments]
ORM_MODEL = User | Token | Advertisments
