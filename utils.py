#  utils.py
#  coding=gbk

from flask import session


# 自定义错误类型
class HttpError(Exception):
    def __init__(self, status, message):  # 顺序！！
        super().__init__()
        self.status_code = status  # 要更改成的状态码
        self.message = message  # 要回复的错误内容

    def show(self):
        return {  # 这里是json的格式，中间要加‘，’
            'status_code': self.status_code,
            'message': self.message
        }


#  确认是否登录
def if_login():
    if session.get('user_id') is None:
        raise HttpError(401, '请先登录')


#  确认是否重名
def if_duplicate_name(username):
    from database import find_username
    valves = find_username(username)
    if valves[0] >= 1:
        raise HttpError(409, '该用户名已被注册')
