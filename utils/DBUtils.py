from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DBUtils:
    # 连接数据库
    engine = create_engine('mysql+pymysql://root:123456@localhost/chat', echo=True)  # 替换为你的数据库连接信息

    @classmethod
    def get_session(cls):
        Session = sessionmaker(bind=cls.engine)
        return Session()

    @classmethod
    def close_session(cls, session):
        session.close()


