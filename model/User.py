from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker

from utils import DBUtils

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    userAccount = Column(String(256), nullable=False, comment='账号')
    userPassword = Column(String(512), nullable=False, comment='密码')
    userName = Column(String(256), comment='用户昵称')
    userAvatar = Column(String(1024), comment='用户头像')
    userProfile = Column(String(512), comment='用户简介')
    userRole = Column(String(256), nullable=False, default='user', comment='用户角色：user/admin/ban')
    createTime = Column(DateTime, default=func.now(), nullable=False, comment='创建时间')
    updateTime = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False, comment='更新时间')
    isDelete = Column(Boolean, default=False, nullable=False, comment='是否删除')

    def __str__(self):
        return f"User(id={self.id}, userAccount={self.userAccount}, userName={self.userName}, userRole={self.userRole})"

    def to_dict(self):
        return {'userAccount': self.userAccount, 'userName': self.userName, 'userRole': self.userRole,
                'userAvatar': self.userAvatar, 'userProfile': self.userProfile}

# 创建表
# Base.metadata.create_all(engine)
