from sqlalchemy import create_engine, Column, Integer,String,DATETIME,DECIMAL, or_, and_,not_,func
from sqlalchemy.orm import declarative_base, sessionmaker

from datetime import datetime


db_url = "mysql+pymysql://geeker:geeker@localhost:3306/fastapi_tutor?charset=utf8mb4"

engine = create_engine(db_url, pool_size= 50, echo=True)

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

Base.metadata.create_all(engine) # 所有表创建 <- 只要数据库存在这个表了，就不会触发，也不会更新表结构
# Order.__table__.create(engine,checkfirst = True)  # 单张表的创建


# 三、【表数据的新增】
'''1.实例化数据库表模型类，得到具体的数据'''
u1 = User( username='清风飞扬' )
print( 'User1的属性：',u1.id,u1.username,u1.create_date,u1.update_date )
u2 = User( username='北大青鸟' )
print( 'User2的属性：',u2.username)

'''2.将实例化好的数据，添加到数据库里'''
# 拿到数据库会话管理工具
Session = sessionmaker( bind=engine
                        ,autoflush=False # 是否开启自动刷新python新增的数据到实际的数据库内存缓存中
                        ,autocommit = False # 不自动提交数据，这个是真正提交到数据库磁盘永久生效的
                        )

session = Session()  # 实例化一个数据库操作会话
# session.add( u1 )  # 新增数据到数据库里
# session.add( u2 )
session.commit()  # 提交，永久生效，注意提交后不能回滚

print(session.query(User).all())
#
# # session.rollback() # 回滚，事务没有提交前，dml操作可以回滚
# session.close()  # 关闭数据操作会话
#
#
# '''
# 等价于sql语句：
# insert into user_info_detail(username) values('清风飞扬');
# insert into user_info_detail(username) values('北大青鸟');
# '''
#
# # 四、【表数据的更改】
# session = Session()  # 实例化一个数据库操作会话
# print(f'{session.query(User)=}, {session.query(User).all()=}')
# session.query(User)\
#     .filter( User.username == '北大青鸟' )\
#     .update( {"username":'沃林数智'
#             , "create_date":"2000-10-10"
#               }  # 同时更新多个字段
#              )
# session.commit()
# '''
# 多个复合条件：
# filter( 条件1,条件2，条件3.. )  # and的关系
#
# filter( or_( 条件1,条件2), not_(条件2),and_(条件1,条件2) )
#
# session.query(表模型).filter(条件1).filter(条件2).filter(条件3) 条件可以拼接成and的关系
#
# or_: 函数里的条件都是 or 的关系
# and_: 函数里的条件是 and 的关系
# not_ : 将条件的结果进行取反
# '''
#
# # 五、【表数据的删除】
# try:
#     session.query( User ).filter( User.username == '清风飞扬' ).delete()  # 只要命中就删除
#     session.commit()
# except:
#     session.rollback()  # 如果报错，就回滚
#
# # 清空数据，并且重置自增主键 truncate table 表名; 无法回滚
# # session.execute( text( "truncate table user_info_detail" ) )  # 直接书写原生的sql语句
# # 可以select、update、delete全部支持



'''1.单表基础查询'''
# ① 单条数据查询 first(),返回的是一个查询结果对象
r1 = session.query(User).first()
print('获取单个查询结果对象：',r1)
print(r1.id,r1.usernmae,r1.create_date,r1.update_date)

# ② 全量查询 all() , 返回的是一个列表list
r2 = session.query(User).all()
print('获取多个查询结果对象：',r2)
for i in range( len(r2) ):
    print(f'第{i+1}行数据：',r2[i].id,r2[i].usernmae,r2[i].create_date,r2[i].update_date)

q = session.query(User)  # 得到一个查询语句对象
r3 = q.all()  # 获取查询语句对象的所有内容
print(q)
print(r3)

# ③ where 条件查询
r4 = session.query(User).filter( or_(User.id == 1, User.usernmae == '李四')  ).all()
for i in r4:
    print(i.id,i.usernmae)

# ④ like模糊匹配查询
r5 = session.query(User).where( User.usernmae.like('%三%') ).all()
for i in r5:
    print('like模糊匹配：',i.id, i.usernmae)

# ⑤ order by排序
r5 = session.query(User).order_by(User.id.desc(), User.usernmae).all()
for i in r5:
    print('排序：', i.id, i.usernmae)

# ⑥ limit 分页
'''
分页公式：
原生sql：limit( (页数-1)*每页数据量, 每页数据量 )
orm里： offset( (页数-1)*每页数据量 ).limit(每页数据量)
'''
n = 1  # 页数
m = 2  # 每页数据量

r6 = session.query(User).offset((n-1)*m).limit(m).all()
for i in r6:
    print('分页：', i.id, i.usernmae)

'''2.分组聚合group by'''
'''
select usernmae,count(1)
from user_info_detail
group by usernmae
having count(1) >= 2
'''
r7 = session.query(User.usernmae,func.count(User.id).label('num')).\
    group_by( User.usernmae ).\
    having( func.count(User.id) >= 2 ).\
    all()

for i in r7:
    print('分组聚合：',i.usernmae,i.num)

'''
func函数支持：max、min、sum、count、avg常用的聚合函数
用法：  func.count(聚合的字段)
'''

'''3.多表关联查询join内连接/outerjoin左连接'''
r8 = session.query(User.id.label('user_id') , User.usernmae, Order.id.label('order_id'), Order.title ).\
    join( Order, User.id == Order.userid ).\
    order_by(User.id).\
    all()

for i in r8:
    print('多表关联内连接：',i.user_id,i.usernmae,i.order_id,i.title)

# outerjoin(谁放在里面，谁就是从表)
r8 = session.query(User.id.label('user_id') , User.usernmae, Order.id.label('order_id'), Order.title ).\
    outerjoin( Order, User.id == Order.userid ).\
    order_by(User.id).\
    all()

for i in r8:
    print('多表关联左连接：',i.user_id,i.usernmae,i.order_id,i.title)

'''
select             ——>   session.query( 表模型名 )
from  表1
join  表2 on 条件  ——> join(连接的表，条件) / outerjoin(连接的表，条件)
where  筛选条件    ——> filter(条件)
group by 分组字段  ——> group_by(分组的字段)
having 分组后过滤  ——> having(过滤的条件)
order by 排序     ——> order_by( 排序的字段.desc() )
limit 分页        ——> offset(偏移量).limit(数据量)
'''

n = 1  # 页数
m = 2  # 每页数据量
r9 = session.query(User.usernmae,Order.title,func.count(1).label('ordernum')).\
    join(Order,User.id == Order.userid).\
    filter(Order.title == '苹果').\
    group_by(User.usernmae,Order.title).\
    having(func.count(1) >= 1).\
    order_by(func.count(1).desc()).\
    offset((n-1)*m).limit(m).\
    all()

for i in r9:
    print('完整的查询：',i.usernmae,i.title,i.ordernum)



