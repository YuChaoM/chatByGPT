from model.Conversation import Conversation
from model.Message import Message
from utils.DBUtils import DBUtils


class ConversationMapper(object):

    def createConversation(self, conversation):
        session = DBUtils.get_session()
        try:
            session.add(conversation)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"错误: {e}")
        finally:
            DBUtils.close_session(session)

    def getAllConversation(self, userId: int):
        session = DBUtils.get_session()
        try:
            all_conversations = session.query(Conversation).filter_by(userId=userId).all()
            return all_conversations
        finally:
            DBUtils.close_session(session)

    def getConversationByPage(self, userId: int, page: int = 1, page_size: int = 10):
        session = DBUtils.get_session()
        try:
            # 计算起始索引
            start_index = (page - 1) * page_size

            # 查询当前页的数据
            conversations_on_page = (
                session.query(Conversation)
                    .filter_by(userId=userId, isDelete=0)
                    .order_by(Conversation.updateTime.desc())
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

    def updateConversation(self, conversation):
        session = DBUtils.get_session()
        try:
            conversation_to_update = session.query(Conversation).filter_by(id=conversation.id).first()
            if conversation_to_update:
                conversation_to_update.title = conversation.title
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"错误: {e}")
        finally:
            DBUtils.close_session(session)

    def deleteConversation(self, id):
        session = DBUtils.get_session()
        try:
            with session.begin():
                conversation_to_update = session.query(Conversation).filter_by(id=id).first()
                if conversation_to_update:
                    conversation_to_update.isDelete = 1
        except Exception as e:
            session.rollback()
            print(f"错误: {e}")
        finally:
            DBUtils.close_session(session)

    def deleteAllMessage(self, id):
        session = DBUtils.get_session()
        try:
            with session.begin():
                messages_to_update = session.query(Message).filter_by(conversationId=id).all()
                for message_to_update in messages_to_update:
                    message_to_update.isDelete = 1
        except Exception as e:
            session.rollback()
            print(f"错误: {e}")
        finally:
            DBUtils.close_session(session)
