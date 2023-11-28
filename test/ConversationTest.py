from mapper.ConversationMapper import ConversationMapper
from model.Conversation import Conversation

conversationMapper = ConversationMapper()

conversation = Conversation()
conversation.title = "test"
conversation.userId = 1

conversationMapper.createConversation(conversation)

list = conversationMapper.getAllConversation(1)
for i in list:
    print(f"conversation ID: {i.id}, title: {i.title}")
    print(i)

# conversation.title = "test1"
# conversation.id = 1
# conversationMapper.updateConversation(conversation)

conv = conversationMapper.getAllConversation(1)
print(f"结果：{conv[0]}")

# conversationMapper.deleteConversation(1)
