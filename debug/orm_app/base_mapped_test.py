from typing import Optional

from sqlalchemy import Column, Integer, create_engine, String, DateTime,func

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeBase, Mapped,mapped_column

from fastapi import APIRouter, Depends
from debug.orm_app.sqlalchemy_full_app import User

from datetime import datetime

db_url = "mysql+pymysql://geeker:geeker@localhost:3306/fastapi_tutor?charset=utf8mb4"

engine = create_engine(db_url)
session = sessionmaker(engine, expire_on_commit=False)

# Base 基类
class Base(DeclarativeBase):
    pass

class MetaBase(Base):
    __tablename__ = "base_mapped_column"
    # id = Column(Integer, primary_key=True)
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True,nullable=False)

    # mapped_column： 默认 nullable=False
    num:Mapped[str] = mapped_column(String(30),unique=True) # 唯一键
    name:Mapped[str] = mapped_column(String(30),default="") #

    name1:Mapped[str] = mapped_column(String(30),nullable=True)
    # name2:Optional[str] = mapped_column(String(30)) # 报错
    name3:Mapped[str | None] = mapped_column(String(30),nullable=True)
    name4:Mapped[Optional[str]] = mapped_column(String(30),nullable=True)


    age:Mapped[int] = mapped_column(Integer,default=18)

    # 默认null
    education:Mapped[str] = mapped_column(String(50),nullable=True)

    create_time:Mapped[datetime] = mapped_column(server_default=func.now())
    update_time:Mapped[datetime] = mapped_column(server_default=func.now(),onupdate=func.now())

    pass


Base.metadata.create_all(engine)
