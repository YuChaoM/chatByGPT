from model.Conversation import Conversation
from model.Message import Message
from utils import DBUtils


class MessageMapper(object):

    def createMessage(self, message):
        DBUtils.session.add(message)
        DBUtils.session.commit()
        DBUtils.session.close()

    def getAllMessage(self, conversationId, userId):
        all_messages = DBUtils.session.query(Message).filter_by(userId=userId, conversationId=conversationId,
                                                                isDelete=0).all()
        return all_messages

    def getMessageByPage(self, conversationId: int, page: int = 1, page_size: int = 10):
        try:
            # 计算起始索引
            start_index = (page - 1) * page_size

            # 查询当前页的数据
            conversations_on_page = (
                DBUtils.session.query(Message)
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

    def updateMessage(self, message):
        message_to_update = DBUtils.session.query(Message).filter_by(id=message.id).first()
        if message_to_update:
            message_to_update.content = message.content
            DBUtils.session.commit()
            DBUtils.session.close()

    def deleteMessage(self, id):
        message_to_update = DBUtils.session.query(Message).filter_by(id=id).first()
        if message_to_update:
            message_to_update.isDelete = 1
            DBUtils.session.commit()
            DBUtils.session.close()

    def deleteAllMessage(self, id):
        message_to_update = DBUtils.session.query(Message).filter_by(id=id).all()
        if message_to_update:
            message_to_update.isDelete = 1
            DBUtils.session.commit()
            DBUtils.session.close()

    def getMessageList(self, conversationId):
        try:
            message_list = (
                DBUtils.session.query(Message)
                    .filter_by(conversationId=conversationId, isDelete=0)
                    .order_by(Message.updateTime.desc())
                    .limit(10)
                    .all()
            )

            return message_list

        except Exception as e:
            # 处理异常
            raise e  # 可以根据需要选择是否重新抛出异常
