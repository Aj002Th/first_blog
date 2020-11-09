#  database.py
#  coding=gbk

import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from utils import HttpError
from flask import session


#  ���ݿ�����
def sql_connect():
    conn = mysql.connector.connect(user='root', password='', database='my_first_sql', buffered=True)
    cursor = conn.cursor()
    return conn, cursor


#  �����û���
def find_username(username):
    conn, cursor = sql_connect()
    sql = 'select count(*) from `users` where `username`=%s'
    cursor.execute(sql, (username,))
    valves = cursor.fetchone()  # ����һ����¼����Ԫ�����ʽ

    conn.commit()

    cursor.close()
    conn.close()

    return valves


# �洢�û�������
def save_user_information(username, password):
    values = find_username(username)
    if values[0] >= 1:
        raise HttpError(409, '���û����ѱ�ע��')

    conn, cursor = sql_connect()

    pwd = generate_password_hash(password)  # ��������м���
    sql = 'insert into `users`(`username`, `password`) values (%s, %s)'
    cursor.execute(sql, (username, pwd))

    conn.commit()

    cursor.close()
    conn.close()


#  ��֤�û�������,�ɹ��򷵻�id
def check_user_information(username, password):
    conn, cursor = sql_connect()
    cursor.execute('select * from `users` where `username`=%s', (username,))
    valves = cursor.fetchone()

    if valves is None:
        raise HttpError(400, '���û��������ڣ�����ע��')

    if not check_password_hash(valves[2], password):
        raise HttpError(400, '�������')

    conn.commit()

    cursor.close()
    conn.close()

    return valves[0]


#  �����û���
def update_username(username):
    conn, cursor = sql_connect()
    cursor.execute('update `users` set `username`=%s where id=%s', (username, session.get('user_id')))

    conn.commit()

    cursor.close()
    conn.close()


#  ��������
def update_password(password):
    conn, cursor = sql_connect()
    sql = 'update `users` set `password`=%s where id=%s'
    cursor.execute(sql, (generate_password_hash(password), session.get('user_id')))

    conn.commit()

    cursor.close()
    conn.close()


#  ���±���
def save_article(user_id, content):
    conn, cursor = sql_connect()
    sql = 'replace into `article_table` (`user_id`, `content`) values (%s, %s)'  # С�޸�
    cursor.execute(sql, (user_id, content))

    conn.commit()

    cursor.close()
    conn.close()


#  �������ݻ�ȡ
def get_article(user_id):
    conn, cursor = sql_connect()
    sql = 'select * from `article_table` where `user_id`=%s'
    cursor.execute(sql, (user_id,))
    content = cursor.fetchone()

    if content is None:
        raise HttpError(404, '����δ��������')

    content = content[2]

    conn.commit()

    cursor.close()
    conn.close()

    return content


# ���������޸�
def revise_article(content, user_id):
    conn, cursor = sql_connect()
    sql = 'update `article_table` set `content`=%s where user_id=%s'
    cursor.execute(sql, (content, user_id))

    conn.commit()

    cursor.close()
    conn.close()
