from flask_cors import CORS
from flask import Flask, Blueprint, jsonify
import configparser
from controller.ConversationController import conversation_api_bp
from controller.MessageController import message_api_bp
from controller.UserController import user_api_bp
from service import AIService

app = Flask(__name__)
CORS(app, supports_credentials=True, )  # 启用携带凭证的支持

# 设置密钥，用于加密会话数据
app.secret_key = 'your_secret_key_yuchao'
# 设置 session 过期时间为3小时，默认过期时间是浏览器会话结束时。这意味着一旦用户关闭浏览器，session 数据将被清除
app.config['PERMANENT_SESSION_LIFETIME'] = 3 * 60 * 60

config = configparser.ConfigParser()
config.read('config.ini')

app.config['APP_ID'] = config.get('credentials', 'APP_ID')
app.config['API_SECRET'] = config.get('credentials', 'API_SECRET')
app.config['API_KEY'] = config.get('credentials', 'API_KEY')

# 注册蓝图
app.register_blueprint(user_api_bp, url_prefix='/api/user')
app.register_blueprint(conversation_api_bp, url_prefix='/api/conversation')
app.register_blueprint(message_api_bp, url_prefix='/api/message')


@app.route('/hello')
def hello():
    return 'Hello, World!'

# 统一处理所有响应
@app.after_request
def after_request(response):
    # 获取 Set-Cookie 头部
    cookies = response.headers.getlist('Set-Cookie')
    print( response.headers)
    print(cookies)
    # 手动检查是否包含 Set-Cookie 头部
    if 'Set-Cookie' in response.headers:
        # 获取 Set-Cookie 头部的值
        cookies = response.headers.getlist('Set-Cookie')

        # 修改其中的 SameSite 和 Secure 属性
        modified_cookies = [cookie + '; SameSite=None; Secure' for cookie in cookies]

        # 将修改后的值设置回 response.headers
        response.headers['Set-Cookie'] = ', '.join(modified_cookies)

    print("------------------")

    return response

# @app.route('/<path:path>', methods=['OPTIONS'])
# def handle_options(path):
#     return jsonify(success=True), 200, {
#         'Access-Control-Allow-Origin': '*',
#         'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
#         'Access-Control-Allow-Headers': 'Content-Type',
#         'Access-Control-Allow-Credentials': 'true',
#     }


if __name__ == '__main__':
    # app.run()
    # 启用https
    # app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))
    # 将 host 参数设置为 '0.0.0.0'，使应用在所有可用的网络接口上监听
    app.run(host='0.0.0.0', port=5000, debug=True)

# openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365