from model.Conversation import Conversation
from model.Message import Message
from utils import DBUtils


class ConversationMapper(object):

    def createConversation(self, conversation):
        DBUtils.session.add(conversation)
        DBUtils.session.commit()
        DBUtils.session.close()

    def getAllConversation(self, userId: int):
        all_conversations = DBUtils.session.query(Conversation).filter_by(userId=userId).all()
        return all_conversations

    def getConversationByPage(self, userId: int, page: int = 1, page_size: int = 10):
        try:
            # 计算起始索引
            start_index = (page - 1) * page_size

            # 查询当前页的数据
            conversations_on_page = (
                DBUtils.session.query(Conversation)
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

    def updateConversation(self, conversation):
        conversation_to_update = DBUtils.session.query(Conversation).filter_by(id=conversation.id).first()
        if conversation_to_update:
            conversation_to_update.title = conversation.title
            DBUtils.session.commit()
            DBUtils.session.close()

    def deleteConversation(self, id):
        try:
            # 开始事务
            with DBUtils.session.begin(subtransactions=True):
                conversation_to_update = DBUtils.session.query(Conversation).filter_by(id=id).first()
                if conversation_to_update:
                    conversation_to_update.isDelete = 1

        except Exception as e:
            # 出现异常时回滚事务
            DBUtils.session.rollback()
            raise e  # 重新抛出异常，以便上层处理

    def deleteAllMessage(self, id):
        try:
            # 开始事务
            with DBUtils.session.begin(subtransactions=True):
                messages_to_update = DBUtils.session.query(Message).filter_by(conversationId=id).all()
                for message_to_update in messages_to_update:
                    message_to_update.isDelete = 1

        except Exception as e:
            # 出现异常时回滚事务
            DBUtils.session.rollback()
            raise e  # 重新抛出异常，以便上层处理
