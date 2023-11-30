import hashlib
from functools import wraps
from flask import session, jsonify

from common.error_responses import ErrorCode


def calculate_md5(input_string):
    # 创建 MD5 对象
    md5 = hashlib.md5()

    # 将字符串转换为字节对象并更新 MD5 对象
    md5.update(input_string.encode('utf-8'))

    # 获取 MD5 哈希值的十六进制表示
    md5_value = md5.hexdigest()

    return md5_value

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_account = session.get("userAccount")
        if not user_account:
            return jsonify({
                'code': ErrorCode.get_code(ErrorCode.NOT_LOGIN_ERROR),
                'data': {},
                'message': ErrorCode.get_message(ErrorCode.NOT_LOGIN_ERROR)
            })
        return f(*args, **kwargs)
    return decorated_function