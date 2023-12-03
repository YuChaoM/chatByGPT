from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker

from utils import DBUtils

Base = declarative_base()


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    conversationId = Column(Integer, nullable=False, comment='会话id')
    content = Column(Text, nullable=False, comment='内容')
    userId = Column(Integer, nullable=False, comment='创建人id')
    createTime = Column(DateTime, default=func.now(), nullable=False, comment='创建时间')
    updateTime = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False, comment='更新时间')
    isDelete = Column(Boolean, default=False, nullable=False, comment='是否删除')

    def __str__(self):
        return f"Message(id={self.id}, conversationId={self.conversationId}, content={self.content}," \
               f"userId={self.userId})"

    def __json__(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'conversationId':self.conversationId,
            'content':self.content,
            'createTime': self.createTime.strftime('%Y-%m-%d %H:%M:%S') if self.createTime else None,
        }

# 创建表
# Base.metadata.create_all(engine)
