from sqlalchemy import Column, Integer, String, DATETIME, create_engine, Boolean,Text,text
from datetime import datetime

# 定义基类模板，解决通用字段
class Template():
    id = Column( Integer  # 声明字段的数据类型
                 , primary_key=True  # 声明是主键
                 , autoincrement=True # 声明是自增主键
                 , comment='订单编号，自增主键'  # 注释
                 )
    create_datetime = Column(DATETIME
                         , default=datetime.now  # 默认值是当前时间
                         )
    update_datetime = Column(DATETIME
                         , default=datetime.now  # 首次创建的时间跟更新时间一致
                         , onupdate=datetime.now
                         )
    is_deleted = Column(Boolean, default=False,server_default=text("0"))
    delete_datetime = Column(DATETIME, nullable=True)
