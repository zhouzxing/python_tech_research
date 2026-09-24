from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from dotenv import load_dotenv
import os

# 指定路径必须是指定路径
load_dotenv(
    dotenv_path=f".env.{os.getenv("ENVIRONMENT",'dev')}",       # 指定 .env 文件路径，默认自动查找， 支持自动从当前目录递归向上查询
    override=False,           # 是否覆盖已存在的环境变量，默认 False
    verbose=False,            # 是否打印调试信息
    encoding="utf-8",         # 文件编码
)

# load_dotenv() # 默认 .env, 递归向上

# .env 解析规则： 必须有空格，多个空格有问题？
db_url = os.getenv("DATABASE_URL")
print(db_url)

key_with_q = os.getenv("KEY_WITH_Q")
print(key_with_q)

key_with_q1 = os.getenv("KEY_WITH_Q1")
print(key_with_q1)

key_with_q2 = os.getenv("KEY_WITH_Q2")
print(key_with_q2)

key_without_q = os.getenv("KEY_WITHOUT_Q")
print(key_without_q)






# engine = create_engine(db_url)

# 三种实现方式皆可！
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
