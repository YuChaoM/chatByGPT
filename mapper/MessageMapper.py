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
