#  app.py
#  coding=gbk

from flask import Flask, jsonify
from users import user_bp
from session import session_bp
from article import article_bp
from config import secret_key
from utils import HttpError
from administrators import administrators_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key  # sessions加密的密钥


# 欢迎界面
@app.route('/')
def welcome():  # 主页面显示
    return 'welcome to your visit!'


# 对错误的处理
@app.errorhandler(HttpError)  # 对HttpError的发生进行捕捉
def error_handle(error):
    response = jsonify(error.show())  # 将自定义错误类型返回的json数据转化成响应，以求能够改写返回的状态码
    response.status_code = error.status_code
    return response


# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(session_bp)
app.register_blueprint(article_bp)
app.register_blueprint(administrators_bp)

# request -> before_request -> route -> after_request中间件


# 让程序运行起来！！！
if __name__ == '__main__':
    app.run()
