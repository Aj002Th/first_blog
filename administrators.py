# administrators.py
# coding=gbk

from flask import Blueprint, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from utils import HttpError
from database import sql_connect


administrators_bp = Blueprint('administrators', __name__, url_prefix='/administrators')


@administrators_bp.route('', methods=['POST'])
def arrange():
    data = request.get_json(force=True)
    password = data.get('password')

    pwd = generate_password_hash('123456')

    if not check_password_hash(pwd, password):
        raise HttpError(400, '密码错误')

    session['administrators'] = 'on'

    return '已通过管理员验证'


#  管理员删除用户的权力
@administrators_bp.route('/delete', methods=['PUT'])
def delete_user():
    if session.get('administrators') is None:
        raise HttpError(401, '请先进行管理员登录')

    data = request.get_json(force=True)
    username = data.get('username')

    conn, cursor = sql_connect()
    cursor.execute('select * from `users` where `username`=%s', (username,))
    valves = cursor.fetchone()

    if valves is None:
        raise HttpError(404, '该用户名不存在，无法删除')
    sql = 'delete from `users` where `username`=%s'
    cursor.execute(sql, (username,))

    conn.commit()

    cursor.close()
    conn.close()

    return '该用户已被删除'
