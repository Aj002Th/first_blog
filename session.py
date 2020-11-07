#  session.py
#  coding=gbk

from flask import Blueprint, request
from database import *
from utils import if_login

session_bp = Blueprint('session', __name__, url_prefix='/session')


@session_bp.route('', methods=['POST'])
def login():
    data = request.get_json(force=True)
    username = data.get('username')
    password = data.get('password')

    user_id = check_user_information(username, password)

    session['username'] = username  # 是session!!拼写
    session['user_id'] = user_id

    return '登录成功！'


@session_bp.route('/show')
def show_information():
    if_login()

    username = session['username']
    user_id = session['user_id']

    return {
        'username': username,
        'user_id': user_id
    }
