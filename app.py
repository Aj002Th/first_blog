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

app.config['SECRET_KEY'] = secret_key  # sessions���ܵ���Կ


# ��ӭ����
@app.route('/')
def welcome():  # ��ҳ����ʾ
    return 'welcome to your visit!'


# �Դ���Ĵ���
@app.errorhandler(HttpError)  # ��HttpError�ķ������в�׽
def error_handle(error):
    response = jsonify(error.show())  # ���Զ���������ͷ��ص�json����ת������Ӧ�������ܹ���д���ص�״̬��
    response.status_code = error.status_code
    return response


# ע����ͼ
app.register_blueprint(user_bp)
app.register_blueprint(session_bp)
app.register_blueprint(article_bp)
app.register_blueprint(administrators_bp)

# request -> before_request -> route -> after_request�м��


# �ó�����������������
if __name__ == '__main__':
    app.run()
