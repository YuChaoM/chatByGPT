from model.Conversation import Conversation
from utils import DBUtils


class ConversationMapper(object):

    def createConversation(self, conversation):
        DBUtils.session.add(conversation)
        DBUtils.session.commit()
        DBUtils.session.close()

    def getAllConversation(self, userId: int):
        all_conversations = DBUtils.session.query(Conversation).filter_by(userId=userId).all()
        return all_conversations

    def updateConversation(self, conversation):
        conversation_to_update = DBUtils.session.query(Conversation).filter_by(id=conversation.id).first()
        if conversation_to_update:
            conversation_to_update.title = conversation.title
            DBUtils.session.commit()
            DBUtils.session.close()

    def deleteConversation(self, id):
        conversation_to_update = DBUtils.session.query(Conversation).filter_by(id=id).first()
        if conversation_to_update:
            DBUtils.session.delete(conversation_to_update)
            DBUtils.session.commit()
            DBUtils.session.close()
