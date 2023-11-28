from mapper.MessageMapper import MessageMapper
from model.Message import Message

messageMapper = MessageMapper()

message = Message()
message.content = "hello world"
message.userId = 1
message.conversationId = 3

messageMapper.createMessage(message)

list = messageMapper.getAllMessage(3, 1)
for i in list:
    print(f"结果{i}")

# message.title = "test1"
# message.id = 1
# messageMapper.updateMessage(message)

# conv = messageMapper.getAllMessage(1)
# print(f"结果：{conv[0]}")

# messageMapper.deleteMessage(1)
