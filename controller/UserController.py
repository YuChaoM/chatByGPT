from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

# 创建蓝图
user_api_bp = Blueprint('user', __name__)
api = Api(user_api_bp)

users = []  # 用于存储用户信息的简单列表（实际项目中应使用数据库）

class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # 简单示例：将用户信息存储在内存中（实际项目中应使用数据库）
        users.append({'username': username, 'password': password})

        return jsonify({'message': 'User registered successfully'})

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # 简单示例：检查用户信息（实际项目中应使用数据库）
        for user in users:
            if user['username'] == username and user['password'] == password:
                return jsonify({'message': 'Login successful'})
        return jsonify({'message': 'Invalid credentials'})

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
