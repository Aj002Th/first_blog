#  database.py
#  coding=gbk

import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from utils import HttpError
from flask import session


#  数据库连接
def sql_connect():
    conn = mysql.connector.connect(user='root', password='', database='my_first_sql', buffered=True)
    cursor = conn.cursor()
    return conn, cursor


#  查找用户名
def find_username(username):
    conn, cursor = sql_connect()
    sql = 'select count(*) from `users` where `username`=%s'
    cursor.execute(sql, (username,))
    valves = cursor.fetchone()  # 返回一条记录，以元组的形式

    conn.commit()

    cursor.close()
    conn.close()

    return valves


# 存储用户名密码
def save_user_information(username, password):
    values = find_username(username)
    if values[0] >= 1:
        raise HttpError(409, '该用户名已被注册')

    conn, cursor = sql_connect()

    pwd = generate_password_hash(password)  # 对密码进行加密
    sql = 'insert into `users`(`username`, `password`) values (%s, %s)'
    cursor.execute(sql, (username, pwd))

    conn.commit()

    cursor.close()
    conn.close()


#  验证用户名密码,成功则返回id
def check_user_information(username, password):
    conn, cursor = sql_connect()
    cursor.execute('select * from `users` where `username`=%s', (username,))
    valves = cursor.fetchone()

    if valves is None:
        raise HttpError(400, '该用户名不存在，请先注册')

    if not check_password_hash(valves[2], password):
        raise HttpError(400, '密码错误')

    conn.commit()

    cursor.close()
    conn.close()

    return valves[0]


#  更新用户名
def update_username(username):
    conn, cursor = sql_connect()
    cursor.execute('update `users` set `username`=%s where id=%s', (username, session.get('user_id')))

    conn.commit()

    cursor.close()
    conn.close()


#  更新密码
def update_password(password):
    conn, cursor = sql_connect()
    sql = 'update `users` set `password`=%s where id=%s'
    cursor.execute(sql, (generate_password_hash(password), session.get('user_id')))

    conn.commit()

    cursor.close()
    conn.close()


#  文章保存
def save_article(user_id, content):
    conn, cursor = sql_connect()
    sql = 'replace into `article_table` (`user_id`, `content`) values (%s, %s)'  # 小修改
    cursor.execute(sql, (user_id, content))

    conn.commit()

    cursor.close()
    conn.close()


#  文章内容获取
def get_article(user_id):
    conn, cursor = sql_connect()
    sql = 'select * from `article_table` where `user_id`=%s'
    cursor.execute(sql, (user_id,))
    content = cursor.fetchone()

    if content is None:
        raise HttpError(404, '你尚未发布文章')

    content = content[2]

    conn.commit()

    cursor.close()
    conn.close()

    return content


# 文章内容修改
def revise_article(content, user_id):
    conn, cursor = sql_connect()
    sql = 'update `article_table` set `content`=%s where user_id=%s'
    cursor.execute(sql, (content, user_id))

    conn.commit()

    cursor.close()
    conn.close()
