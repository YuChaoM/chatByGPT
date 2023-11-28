from flask import Flask, Blueprint

from controller.UserController import user_api_bp

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(user_api_bp, url_prefix='/api/user')

@app.route('/hello')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
