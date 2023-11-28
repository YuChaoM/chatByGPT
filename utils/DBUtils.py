from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 连接数据库
engine = create_engine('mysql+pymysql://root:123456@localhost/chat', echo=True)  # 替换为你的数据库连接信息

# # 创建表
# Base.metadata.create_all(engine)

# 创建数据库会话
Session = sessionmaker(bind=engine)
session = Session()

# 关闭会话
session.close()
