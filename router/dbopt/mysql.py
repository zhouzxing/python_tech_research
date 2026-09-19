from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer,String,DATETIME,DECIMAL
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

from typing import Annotated
from fastapi import Depends, FastAPI,APIRouter,Form,File,UploadFile
from fastapi.security import OAuth2PasswordRequestForm

route = APIRouter(prefix="/mysql",tags=["mysql"])

db_url = "mysql+pymysql://geeker:geeker@localhost:3306/fastapi_tutor?charset=utf8mb4"
engine = create_engine(db_url, pool_size= 50, echo=True)
Session = sessionmaker( bind=engine
                        ,autoflush=False # 是否开启自动刷新python新增的数据到实际的数据库内存缓存中
                        ,autocommit = False # 不自动提交数据，这个是真正提交到数据库磁盘永久生效的 -> 2.0 不支持True自动提交
                        )

session = Session()  # 实例化一个数据库操作会话


Base = declarative_base() # 获取基类！

class Order(Base):   # python里的表名字
    __tablename__ = 'order_info_detail'  # 实际数据库的表名字
    id = Column( Integer  # 声明字段的数据类型
                 , primary_key=True  # 声明是主键
                 , autoincrement=True # 声明是自增主键
                 , comment='订单编号，自增主键'  # 注释
                 )
    title = Column( String(50)  # 对应数据库的varchar类型
                    ,nullable=False  # 不允许为null
                    )
    price = Column(DECIMAL)
    userid = Column( Integer
                     # ,ForeignKey('user_info_detail.id')
                     ,nullable=False )  # 外键约束
    create_date = Column(DATETIME
                         , default=datetime.now  # 默认值是当前时间
                         )
    update_date = Column(DATETIME
                         , default=datetime.now  # 首次创建的时间跟更新时间一致
                         , onupdate=datetime.now
                         )

class User(Base):   # python里的表名字
    __tablename__ = 'user_info_detail'  # 实际数据库的表名字
    id = Column( Integer  # 声明字段的数据类型
                 , primary_key=True  # 声明是主键
                 , autoincrement=True # 声明是自增主键
                 , comment='用户编号，自增主键'  # 注释
                 )
    username = Column( String(50)  # 对应数据库的varchar类型
                    ,nullable=False  # 不允许为null
                    ,comment='用户名'
                    )
    create_date = Column(DATETIME
                         , default=datetime.now  # 默认值是当前时间
                         )
    update_date = Column(DATETIME
                         , default=datetime.now  # 首次创建的时间跟更新时间一致
                         , onupdate=datetime.now
                         )


@route.get("/user")
def user_detail_info():
    return session.query(User).all()

@route.post("/user")
def user_detail_info(username:str):
    session.add(User(username=username))
    return session.query(User).all()
