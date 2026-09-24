from sqlalchemy import Column, Integer, create_engine, String, ForeignKey,DATETIME,DateTime,func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker,declarative_base,DeclarativeBase

from fastapi import APIRouter, Depends
from debug.orm_app.sqlalchemy_full_app import User

from datetime import datetime


db_url = "mysql+pymysql://geeker:geeker@localhost:3306/fastapi_tutor?charset=utf8mb4"

engine = create_engine(db_url)
session = sessionmaker(engine, expire_on_commit=False)

# 外键引用
Base = declarative_base()
class MetaBaseFunc(Base):
    __tablename__ = "meta_base_func"
    id = Column(Integer, primary_key=True)
    pass

# Base.metadata.create_all(engine)
# Base 基类 - 可行，但不建议用多个Base分别创建表
# class Base(DeclarativeBase):
#     pass

class MetaBase(Base):
    __tablename__ = "base_column_test"
    id = Column(Integer, primary_key=True)
    num = Column(String(30),nullable=False,unique=True)
    name = Column(String(30),nullable=False,default="")

    # null
    education = Column(String(50), nullable=True)

    # 索引与外键 - 运行时查找
    f_id = Column(Integer,ForeignKey("meta_base_func.id"),nullable=False, index=True)
    fd_id = Column(Integer,ForeignKey("meta_base_func.id"),nullable=True)


    # 日期处理
    create_date = Column(DATETIME
                         , default=datetime.now  # 默认值是当前时间
                         )
    create_date1 = Column(DateTime, default=datetime.utcnow())

    update_date = Column(DATETIME
                         , default=datetime.now  # 首次创建的时间跟更新时间一致
                         , onupdate=datetime.now
                         )

    # 默认值处理
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    update_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

Base.metadata.create_all(engine)

