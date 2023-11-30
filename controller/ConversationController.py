import hashlib

from flask import Blueprint, request, jsonify, session
from flask_restful import Api, Resource, reqparse

# 创建蓝图
from common.error_responses import ErrorCode
from controller.UserController import get_logged_user
from mapper.ConversationMapper import ConversationMapper
from mapper.MessageMapper import MessageMapper
from mapper.UserMapper import UserMapper
from model.Conversation import Conversation
from utils import DBUtils
from utils.common_utils import calculate_md5, login_required

conversation_api_bp = Blueprint('conversation', __name__)
api = Api(conversation_api_bp)

conversationMapper = ConversationMapper()
messageMapper = MessageMapper()
userMapper = UserMapper()


class CreateConversation(Resource):
    @login_required
    def post(self):
        data = request.get_json()

        if not data:
            return {'code': ErrorCode.get_code(ErrorCode.PARAMS_ERROR), 'data': {},
                    'message': ErrorCode.get_message(ErrorCode.PARAMS_ERROR)}

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help='title cannot be blank')

        title = data['title']
        userAccount = get_logged_user()
        user = userMapper.getUserByUserAccount(userAccount)
        if not user:
            return {'code': ErrorCode.get_code(ErrorCode.NOT_LOGIN_ERROR), 'data': {},
                    'message': ErrorCode.get_message(ErrorCode.NOT_LOGIN_ERROR)}
        conversation = Conversation()
        conversation.userId = user.id
        conversation.title = title
        conversationMapper.createConversation(conversation)

        return jsonify({
            'code': ErrorCode.get_code(ErrorCode.SUCCESS),
            'data': {},
            'message': ErrorCode.get_message(ErrorCode.SUCCESS)
        })


class updateConversation(Resource):
    @login_required
    def post(self):
        data = request.get_json()

        if not data:
            return {'code': ErrorCode.get_code(ErrorCode.PARAMS_ERROR), 'data': {},
                    'message': ErrorCode.get_message(ErrorCode.PARAMS_ERROR)}

        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True, help='id cannot be blank')
        parser.add_argument('title', type=str, required=True, help='title cannot be blank')

        title = data['title']
        id = data['id']
        conversation = Conversation()
        conversation.id = id
        conversation.title = title
        conversationMapper.updateConversation(conversation)

        return jsonify({
            'code': ErrorCode.get_code(ErrorCode.SUCCESS),
            'data': {},
            'message': ErrorCode.get_message(ErrorCode.SUCCESS)
        })


class deleteConversation(Resource):
    @login_required
    def post(self):
        data = request.get_json()

        if not data:
            return {'code': ErrorCode.get_code(ErrorCode.PARAMS_ERROR), 'data': {},
                    'message': ErrorCode.get_message(ErrorCode.PARAMS_ERROR)}

        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True, help='id cannot be blank')
        id = data['id']
        try:
            conversationMapper.deleteConversation(id)
            conversationMapper.deleteAllMessage(id)
            DBUtils.session.commit()
        except Exception as e:
            DBUtils.session.rollback()
            # 处理异常
            return jsonify({
                'code': ErrorCode.get_code(ErrorCode.SYSTEM_ERROR),
                'data': {},
                'message': ErrorCode.get_message(ErrorCode.SYSTEM_ERROR)
            })
        finally:
            DBUtils.session.close()

        return jsonify({
            'code': ErrorCode.get_code(ErrorCode.SUCCESS),
            'data': {},
            'message': ErrorCode.get_message(ErrorCode.SUCCESS)
        })


class getConversationByPage(Resource):
    @login_required
    def get(self):
        data = request.get_json()

        if not data:
            return {'code': ErrorCode.get_code(ErrorCode.PARAMS_ERROR), 'data': {},
                    'message': ErrorCode.get_message(ErrorCode.PARAMS_ERROR)}

        parser = reqparse.RequestParser()
        parser.add_argument('userId', type=str, required=True, help='userId cannot be blank')
        userId = data['userId']
        pageNum = int(data.get('pageNum', 1))
        pageSize = int(data.get('pageSize', 10))

        try:
            conversations_on_page = conversationMapper.getConversationByPage(userId, pageNum, pageSize)

            # 使用列表推导式调用 __json__ 方法进行序列化
            serialized_conversations = [conversation.__json__() for conversation in conversations_on_page]

            return {'code': ErrorCode.get_code(ErrorCode.SUCCESS),
                    'data': serialized_conversations,
                    'message': ErrorCode.get_message(ErrorCode.SUCCESS)}

        except Exception as e:
            print(e)
            # 在这里处理异常并返回适当的错误响应
            return {'code': ErrorCode.get_code(ErrorCode.SYSTEM_ERROR),
                    'data': {},
                    'message': ErrorCode.get_message(ErrorCode.SYSTEM_ERROR)}


api.add_resource(CreateConversation, '/add')
api.add_resource(updateConversation, '/update')
api.add_resource(deleteConversation, '/delete')
api.add_resource(getConversationByPage, '/get/page')
