#  users.py
#  coding=gbk
from flask import Blueprint, request, session
from database import save_user_information, update_password, update_username
from utils import if_login, if_duplicate_name, HttpError

user_bp = Blueprint('user', __name__, url_prefix='/users')


@user_bp.route('', methods=['POST'])
def register():
    data = request.get_json(force=True)  # �����������е�����
    username = data.get('username')
    password = data.get('password')

    save_user_information(username, password)

    return 'ע��ɹ���'


@user_bp.route('/username', methods=['PUT'])
def change_username():
    data = request.get_json(force=True)
    username = data.get('username')

    if_login()
    if_duplicate_name(username)

    update_username(username)

    session['username'] = username

    return '�û����޸ĳɹ���'


@user_bp.route('/password', methods=['PUT'])
def change_password():
    data = request.get_json(force=True)
    password = data.get('password')

    if session.get('user_id') is None:
        raise HttpError(401, '���ȵ�¼')

    update_password(password)

    return '�����޸ĳɹ���'
