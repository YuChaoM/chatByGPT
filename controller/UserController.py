import hashlib

from flask import Blueprint, request, jsonify, session
from flask_restful import Api, Resource, reqparse

# 创建蓝图
from common.error_responses import ErrorCode
from mapper.UserMapper import UserMapper
from model.User import User
from utils.common_utils import calculate_md5

user_api_bp = Blueprint('user', __name__)
api = Api(user_api_bp)

SALT = "YUCHAO"
userMapper = UserMapper()


class Register(Resource):
    def post(self):
        data = request.get_json()

        if not data or 'userAccount' not in data or 'userPassword' not in data:
            return {'code': ErrorCode.get_code(ErrorCode.PARAMS_ERROR), 'data': {},
                    'message': ErrorCode.get_message(ErrorCode.PARAMS_ERROR)}

        parser = reqparse.RequestParser()
        parser.add_argument('userAccount', type=str, required=True, help='Account cannot be blank')
        parser.add_argument('userPassword', type=str, required=True, help='Password cannot be blank')

        # Parse the JSON data
        # args = parser.parse_args(req=data)

        userAccount = data['userAccount']
        password = data['userPassword']

        # 检查账号是否已存在
        userMapper = UserMapper()
        user = userMapper.getUserByUserAccount(userAccount)
        if user:
            response = {
                'code': ErrorCode.get_code(ErrorCode.PARAMS_ERROR),
                'data': {},
                'message': "账号已存在"
            }
            return jsonify(response)

        user = User()
        user.userName = userAccount
        user.userAccount = userAccount
        userPassword = calculate_md5(password + SALT)  # 获取一个MD5的加密算法对象
        user.userPassword = userPassword
        user.userRole = "user"
        userMapper.createUser(user)

        return jsonify({
            'code': ErrorCode.get_code(ErrorCode.SUCCESS),
            'data': {},
            'message': ErrorCode.get_message(ErrorCode.SUCCESS)
        })


class Login(Resource):
    def post(self):
        data = request.get_json()

        if not data or 'userAccount' not in data or 'userPassword' not in data:
            return {'code': ErrorCode.get_code(ErrorCode.PARAMS_ERROR), 'data': {},
                    'message': ErrorCode.get_message(ErrorCode.PARAMS_ERROR)}

        parser = reqparse.RequestParser()
        parser.add_argument('userAccount', type=str, required=True, help='Account cannot be blank')
        parser.add_argument('userPassword', type=str, required=True, help='Password cannot be blank')

        userAccount = data['userAccount']
        password = data['userPassword']

        user = userMapper.getUserByUserAccount(userAccount)
        if user is None:
            response = {
                'code': ErrorCode.get_code(ErrorCode.PARAMS_ERROR),
                'data': {},
                'message': "账号不存在"
            }
            return jsonify(response)

        password = calculate_md5(password + SALT)
        if user.userPassword == password:
            # 登陆成功，保存登录态
            session["userAccount"] = user.userAccount
            return jsonify({
                'code': ErrorCode.get_code(ErrorCode.SUCCESS),
                'data': {},
                'message': ErrorCode.get_message(ErrorCode.SUCCESS)
            })
        else:
            return jsonify({
                'code': ErrorCode.get_code(ErrorCode.PARAMS_ERROR),
                'data': {},
                'message': "密码错误"
            })


class Logout(Resource):
    def post(self):
        if 'userAccount' not in session:
            return jsonify({
                'code': ErrorCode.get_code(ErrorCode.NOT_LOGIN_ERROR),
                'data': {},
                'message': ErrorCode.get_message(ErrorCode.NOT_LOGIN_ERROR)
            })
        # 清除会话数据
        session.pop('userAccount', None)
        return jsonify({
            'code': ErrorCode.get_code(ErrorCode.SUCCESS),
            'data': {},
            'message': ErrorCode.get_message(ErrorCode.SUCCESS)
        })


class LoginUser(Resource):
    def get(self):
        userAccount = get_logged_user()
        if userAccount:
            user = userMapper.getUserByUserAccount(userAccount)
            return jsonify({
                'code': ErrorCode.get_code(ErrorCode.SUCCESS),
                'data': user.to_dict(),
                'message': ErrorCode.get_message(ErrorCode.SUCCESS)
            })
        else:
            return jsonify({
                'code': ErrorCode.get_code(ErrorCode.NOT_LOGIN_ERROR),
                'data': {},
                'message': ErrorCode.get_message(ErrorCode.NOT_LOGIN_ERROR)
            })


def is_user_logged_in():
    # 检查用户是否已登录
    return 'userAccount' in session


def get_logged_user():
    # 获取已登录用户的信息
    if is_user_logged_in():
        userAccount = session['userAccount']
        return userAccount
    return None


api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(LoginUser, '/get/loginUser')
