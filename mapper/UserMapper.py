from model.User import User
from utils import DBUtils


class UserMapper(object):

    def createUser(self, user):
        DBUtils.session.add(user)
        DBUtils.session.commit()
        DBUtils.session.close()

    def getAllUser(self):
        all_users = DBUtils.session.query(User).all()
        return all_users

    def getUserById(self, id):
        user = DBUtils.session.query(User).filter_by(id=id).first()
        return user

    def getUserByUserAccount(self, userAccount):
        user = DBUtils.session.query(User).filter_by(userAccount=userAccount).first()
        return user

    def updateUser(self, user):
        user_to_update = DBUtils.session.query(User).filter_by(id=user.id).first()
        if user_to_update:
            user_to_update.userName = user.userName
            user_to_update.userAvatar = user.userAvatar
            user_to_update.userProfile = user.userProfile
            DBUtils.session.commit()
            DBUtils.session.close()

    def deleteUser(self, id):
        user_to_update = DBUtils.session.query(User).filter_by(id=id).first()
        if user_to_update:
            DBUtils.session.delete(user_to_update)
            DBUtils.session.commit()
            DBUtils.session.close()
