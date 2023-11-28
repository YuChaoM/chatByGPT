from mapper.UserMapper import UserMapper
from model.User import User

userMapper = UserMapper()

# userMapper.createUser()

# 示例：添加用户
new_user = User(
    userAccount='yuchao',
    userPassword='123456',
    userName='User',
    userAvatar='avatar_url',
    userProfile='profile text',
    userRole='admin'
)
# userMapper.createUser(new_user)

all_users = userMapper.getAllUser()
for user in all_users:
    print(f"User ID: {user.id}, Account: {user.userAccount}, Name: {user.userName}")
    print(user)

new_user.id = 1
userMapper.updateUser(new_user)

# userMapper.deleteUser(2)
