#  article.py
#  coding=gbk

from flask import Blueprint, request, session
from database import save_article, get_article, revise_article
from utils import if_login

article_bp = Blueprint('article', __name__, url_prefix='/article')


@article_bp.route('/post', methods=['POST'])
def post_article():
    data = request.get_json(force=True)
    content = data.get('content')
    user_id = session.get('user_id')
    if_login()

    save_article(user_id, content)
    return '文章发布成功！'


@article_bp.route('/show')
def show_article():
    if_login()

    user_id = session.get('user_id')
    content = get_article(user_id)

    return content


# 修改文章
@article_bp.route('/change', methods=['POST'])
def change_article():
    data = request.get_json(force=True)
    content = data.get('content')
    user_id = session.get('user_id')
    if_login()

    revise_article(content, user_id)

    return '文章修改成功！'

