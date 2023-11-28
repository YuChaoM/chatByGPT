from flask import Flask, Blueprint

from controller.UserController import user_api_bp

app = Flask(__name__)

# 设置密钥，用于加密会话数据
app.secret_key = 'your_secret_key_yuchao'
# 设置 session 过期时间为3小时，默认过期时间是浏览器会话结束时。这意味着一旦用户关闭浏览器，session 数据将被清除
app.config['PERMANENT_SESSION_LIFETIME'] = 3 * 60 * 60

# 注册蓝图
app.register_blueprint(user_api_bp, url_prefix='/api/user')


@app.route('/hello')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    # app.run()
    # 将 host 参数设置为 '0.0.0.0'，使应用在所有可用的网络接口上监听
    app.run(host='0.0.0.0', port=5000, debug=True)
