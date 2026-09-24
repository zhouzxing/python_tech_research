from pydantic import BaseModel
from sqlalchemy.orm import declarative_base,sessionmaker,Session
from sqlalchemy import Column, Integer,String,DATETIME,create_engine
from datetime import datetime

db_url = "mysql+pymysql://geeker:geeker@127.0.0.1:3306/fastapi_tutor?charset=utf8mb4"
engine = create_engine(db_url)


def get_session():
    # Session = sessionmaker(bind=engine
    #                        , autoflush=False
    #                        , autocommit=False
    #                        )

    # session = Session(engine)
    # try:
    #     yield session
    # finally:
    #     session.close()

    with Session()  as session:
        yield session

    # with Session(engine)  as session:
    #     yield session

Base = declarative_base()  # 执行函数，返回一个基类

from model.template import Template

class Order(Base,Template):   # python里的表名字
    __tablename__ = 'order_info_bool_tinyint'  # 实际数据库的表名字
    title = Column( String(50)  # 对应数据库的varchar类型
                    ,nullable=False  # 不允许为null
                    )
    userid = Column( Integer
                     # ,ForeignKey('user_info_detail.id')
                     ,nullable=False )  # 外键约束

# class Order(Base):   # python里的表名字
#     __tablename__ = 'order_info_detail'  # 实际数据库的表名字
#     id = Column( Integer  # 声明字段的数据类型
#                  , primary_key=True  # 声明是主键
#                  , autoincrement=True # 声明是自增主键
#                  , comment='订单编号，自增主键'  # 注释
#                  )
#     title = Column( String(50)  # 对应数据库的varchar类型
#                     ,nullable=False  # 不允许为null
#                     )
#     userid = Column( Integer
#                      # ,ForeignKey('user_info_detail.id')
#                      ,nullable=False )  # 外键约束
#     create_date = Column(DATETIME
#                          , default=datetime.now  # 默认值是当前时间
#                          )
#     update_date = Column(DATETIME
#                          , default=datetime.now  # 首次创建的时间跟更新时间一致
#                          , onupdate=datetime.now
#                          )

# 定义创建订单的请求体模型
class OrderRequest(BaseModel):
    id:int|None = None
    title:str|None = None
    userid:int|None =None

# todo 序列化问题： Order - Base 无法直接序列
class OrderSchema(BaseModel):
    id:int
    title:str
    userid:int
    create_date:datetime
    update_date:datetime

class OrderResponse(BaseModel):

    status_code:str = 200
    detail:str = 'succeed!'
    total:int = 1
    # data:str|dict|list[OrderSchema] # 响应数据
    data:str|dict|list[object] # 响应数据


Order.__table__.create(engine,checkfirst = True)
