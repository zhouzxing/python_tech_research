from sqlalchemy import Column, Integer,create_engine

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker,declarative_base,DeclarativeBase

from fastapi import APIRouter, Depends
from debug.orm_app.sqlalchemy_full_app import User


db_url = "mysql+pymysql://geeker:geeker@localhost:3306/fastapi_tutor?charset=utf8mb4"

engine = create_engine(db_url)

# 测试autoflush - True
session = sessionmaker(engine, autoflush=True ,expire_on_commit=False)

# Base 基类
class Base(DeclarativeBase):
    pass

class MetaBase(Base):
    __tablename__ = "base_autoflush"
    id = Column(Integer, primary_key=True)
    pass

Base.metadata.create_all(engine)


