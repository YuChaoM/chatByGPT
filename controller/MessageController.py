import hashlib

from flask import Blueprint, request, jsonify, session, current_app
from flask_restful import Api, Resource, reqparse

# 创建蓝图
from common.error_responses import ErrorCode
from controller.UserController import get_logged_user
from mapper.MessageMapper import MessageMapper
from mapper.MessageMapper import MessageMapper
from mapper.UserMapper import UserMapper
from model.Message import Message
from service import AIService
from service.AIService import initialize_spark_api, send
from utils import DBUtils
from utils.common_utils import calculate_md5, login_required

message_api_bp = Blueprint('message', __name__)
api = Api(message_api_bp)

messageMapper = MessageMapper()
userMapper = UserMapper()

SYSTEM_USER = 0


class SendMessage(Resource):
    @login_required
    def post(self):
        data = request.get_json()

        if not data:
            return {'code': ErrorCode.get_code(ErrorCode.PARAMS_ERROR), 'data': {},
                    'message': ErrorCode.get_message(ErrorCode.PARAMS_ERROR)}

        parser = reqparse.RequestParser()
        parser.add_argument('conversationId', type=str, required=True, help='conversationId cannot be blank')
        parser.add_argument('content', type=str, required=True, help='content cannot be blank')

        conversationId = data['conversationId']
        content = data['content']
        userAccount = get_logged_user()
        user = userMapper.getUserByUserAccount(userAccount)
        if not user:
            return {'code': ErrorCode.get_code(ErrorCode.NOT_LOGIN_ERROR), 'data': {},
                    'message': ErrorCode.get_message(ErrorCode.NOT_LOGIN_ERROR)}
        # 1.先把提问存到数据库
        try:
            message = Message()
            message.userId = user.id
            message.conversationId = conversationId
            message.content = content
            messageMapper.createMessage(message)
        except Exception as e:
            DBUtils.session.rollback()
            # 处理异常
            return jsonify({
                'code': ErrorCode.get_code(ErrorCode.SYSTEM_ERROR),
                'data': {},
                'message': ErrorCode.get_message(ErrorCode.SYSTEM_ERROR)
            })

        # 2. 调用认知大模型
        print("我:" + content, end="")
        message_list = messageMapper.getMessageList(conversationId)
        answer = send(message_list)

        # 将回答保存到数据库
        try:
            message = Message()
            message.userId = SYSTEM_USER
            message.conversationId = conversationId
            message.content = answer
            messageMapper.createMessage(message)
        except Exception as e:
            DBUtils.session.rollback()
            # 处理异常
            return jsonify({
                'code': ErrorCode.get_code(ErrorCode.SYSTEM_ERROR),
                'data': {},
                'message': ErrorCode.get_message(ErrorCode.SYSTEM_ERROR)
            })

        return jsonify({
            'code': ErrorCode.get_code(ErrorCode.SUCCESS),
            'data': answer,
            'message': ErrorCode.get_message(ErrorCode.SUCCESS)
        })


class getMessageByPage(Resource):
    @login_required
    def get(self):
        data = request.get_json()

        if not data:
            return {'code': ErrorCode.get_code(ErrorCode.PARAMS_ERROR), 'data': {},
                    'message': ErrorCode.get_message(ErrorCode.PARAMS_ERROR)}

        parser = reqparse.RequestParser()
        parser.add_argument('conversationId', type=str, required=True, help='conversationId cannot be blank')
        conversationId = data['conversationId']
        pageNum = int(data.get('pageNum', 1))
        pageSize = int(data.get('pageSize', 10))

        try:
            messages_on_page = messageMapper.getMessageByPage(conversationId, pageNum, pageSize)

            # 使用列表推导式调用 __json__ 方法进行序列化
            serialized_messages = [message.__json__() for message in messages_on_page]

            return {'code': ErrorCode.get_code(ErrorCode.SUCCESS),
                    'data': serialized_messages,
                    'message': ErrorCode.get_message(ErrorCode.SUCCESS)}

        except Exception as e:
            print(e)
            # 在这里处理异常并返回适当的错误响应
            return {'code': ErrorCode.get_code(ErrorCode.SYSTEM_ERROR),
                    'data': {},
                    'message': ErrorCode.get_message(ErrorCode.SYSTEM_ERROR)}


api.add_resource(SendMessage, '/send')
api.add_resource(getMessageByPage, '/get/page')
