# -*- coding: utf-8 -*-#
# filename:index_news.py
# __author__ = 'wanglina'
import json
import pymongo
from flask import Blueprint, render_template
from connect import conn
from longwang.mongodb_news import search_news_db, get_head_image, image_server, datetime_op, get_images, \
    get_mongodb_dict
from bson import ObjectId

db = conn.mongo_conn()
db_redis = conn.redis_conn()

kbg_page = Blueprint('kbg_page', __name__, template_folder='templates')


# 二级频道首页
@kbg_page.route('/kbg/')
def kbg_index():
    return render_template('kbg/kbg_index.html')


# 二级频道列表
@kbg_page.route('/kbg/list/')
def kbg_list():
    return render_template('kbg/kbg_list.html')
