from model.Conversation import Conversation
from model.Message import Message
from utils.DBUtils import DBUtils


class MessageMapper(object):

    def createMessage(self, message):
        session = DBUtils.get_session()
        try:
            session.add(message)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"错误: {e}")
        finally:
            DBUtils.close_session(session)

    def getAllMessage(self, conversationId, userId):
        session = DBUtils.get_session()
        try:
            all_messages = session.query(Message).filter_by(userId=userId, conversationId=conversationId, isDelete=0).all()
            return all_messages
        finally:
            DBUtils.close_session(session)

    def getMessageByPage(self, conversationId: int, page: int = 1, page_size: int = 10):
        session = DBUtils.get_session()
        try:
            # 计算起始索引
            start_index = (page - 1) * page_size

            # 查询当前页的数据
            conversations_on_page = (
                session.query(Message)
                    .filter_by(conversationId=conversationId, isDelete=0)
                    .order_by(Message.updateTime.desc())
                    .limit(page_size)
                    .offset(start_index)
                    .all()
            )

            return conversations_on_page

        except Exception as e:
            # 处理异常
            raise e  # 可以根据需要选择是否重新抛出异常
        finally:
            DBUtils.close_session(session)

    def updateMessage(self, message):
        session = DBUtils.get_session()
        try:
            message_to_update = session.query(Message).filter_by(id=message.id).first()
            if message_to_update:
                message_to_update.content = message.content
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"错误: {e}")
        finally:
            DBUtils.close_session(session)

    def deleteMessage(self, id):
        session = DBUtils.get_session()
        try:
            message_to_update = session.query(Message).filter_by(id=id).first()
            if message_to_update:
                message_to_update.isDelete = 1
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"错误: {e}")
        finally:
            DBUtils.close_session(session)

    def deleteAllMessage(self, id):
        session = DBUtils.get_session()
        try:
            message_to_update = session.query(Message).filter_by(id=id).all()
            if message_to_update:
                message_to_update.isDelete = 1
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"错误: {e}")
        finally:
            DBUtils.close_session(session)

    def getMessageList(self, conversationId):
        session = DBUtils.get_session()
        try:
            message_list = (
                session.query(Message)
                    .filter_by(conversationId=conversationId, isDelete=0)
                    .order_by(Message.updateTime.desc())
                    .limit(10)
                    .all()
            )

            return message_list

        except Exception as e:
            # 处理异常
            raise e  # 可以根据需要选择是否重新抛出异常
        finally:
            DBUtils.close_session(session)
