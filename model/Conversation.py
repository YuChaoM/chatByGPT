from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker

from utils import DBUtils

Base = declarative_base()


class Conversation(Base):
    __tablename__ = 'conversation'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    userId = Column(Integer, nullable=False, comment='创建人id')
    title = Column(String(256), nullable=False, comment='标题')
    createTime = Column(DateTime, default=func.now(), nullable=False, comment='创建时间')
    updateTime = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False, comment='更新时间')
    isDelete = Column(Boolean, default=False, nullable=False, comment='是否删除')

    def __str__(self):
        return f"Conversation(id={self.id}, userId={self.userId}, title={self.title})"

# 创建表
# Base.metadata.create_all(engine)
