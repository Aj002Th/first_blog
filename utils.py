#  utils.py
#  coding=gbk

from flask import session


# �Զ����������
class HttpError(Exception):
    def __init__(self, status, message):  # ˳�򣡣�
        super().__init__()
        self.status_code = status  # Ҫ���ĳɵ�״̬��
        self.message = message  # Ҫ�ظ��Ĵ�������

    def show(self):
        return {  # ������json�ĸ�ʽ���м�Ҫ�ӡ�����
            'status_code': self.status_code,
            'message': self.message
        }


#  ȷ���Ƿ��¼
def if_login():
    if session.get('user_id') is None:
        raise HttpError(401, '���ȵ�¼')


#  ȷ���Ƿ�����
def if_duplicate_name(username):
    from database import find_username
    valves = find_username(username)
    if valves[0] >= 1:
        raise HttpError(409, '���û����ѱ�ע��')
