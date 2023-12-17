from model.User import User
from utils.DBUtils import DBUtils


class UserMapper(object):

    def createUser(self, user):
        session = DBUtils.get_session()
        try:
            session.add(user)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"错误: {e}")
        finally:
            DBUtils.close_session(session)

    def getAllUser(self):
        session = DBUtils.get_session()
        try:
            all_users = session.query(User).all()
        finally:
            DBUtils.close_session(session)
        return all_users

    def getUserById(self, id):
        session = DBUtils.get_session()
        try:
            user = session.query(User).filter_by(id=id).first()
        finally:
            DBUtils.close_session(session)
        return user

    def getUserByUserAccount(self, userAccount):
        user = None  # 初始化 user 变量
        session = DBUtils.get_session()

        try:
            # 在这里执行数据库操作
            user = session.query(User).filter_by(userAccount=userAccount).first()
        except Exception as e:
            session.rollback()
            print(f"错误: {e}")
        finally:
            DBUtils.close_session(session)
        return user

    def updateUser(self, user):
        session = DBUtils.get_session()
        try:
            user_to_update = session.query(User).filter_by(id=user.id).first()
            if user_to_update:
                user_to_update.userName = user.userName
                user_to_update.userAvatar = user.userAvatar
                user_to_update.userProfile = user.userProfile
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"错误: {e}")
        finally:
            DBUtils.close_session(session)

    def deleteUser(self, id):
        session = DBUtils.get_session()
        try:
            user_to_delete = session.query(User).filter_by(id=id).first()
            if user_to_delete:
                session.delete(user_to_delete)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"错误: {e}")
        finally:
            DBUtils.close_session(session)
