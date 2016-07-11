# -*- coding: utf-8 -*-#
# filename:psd_views.py

import json
import pymongo
from flask import Blueprint, render_template
from connect import conn
from longwang.mongodb_news import get_image_news, search_news_db, get_head_image, image_server, datetime_op, get_images, \
    get_mongodb_dict
from bson import ObjectId

db = conn.mongo_conn()
db_redis = conn.redis_conn()

psd_page = Blueprint('psd_page', __name__, template_folder='templates')


# 二级频道首页
@psd_page.route('/psd/')
def psd_index():
    # 轮换图
    lht = get_head_image(ObjectId("57688f50dcc88e552361ba27"), 4)
    # 头条新闻
    ttxw = get_image_news("577c646159f0d8efacae7e65", 6)
    # 今日热评文字1
    jrrp_1 = get_image_news("577c647559f0d8efacae7e68", 1)
    # 今日热评图片1
    jrrp_2 = get_image_news("577c647559f0d8efacae7e68", 1, jrrp_1)
    # 今日热评文字3
    jrrp_5 = get_image_news("577c647559f0d8efacae7e68", 3, jrrp_1 + jrrp_2)
    # 独家视界
    djsj = get_image_news("577c648559f0d8efacae7e6b", 10)
    # 当事者说
    dszs = get_image_news("577c649059f0d8efacae7e6e", 3)
    # 排行24
    ph_24 = get_image_news("576b37b8a6d2e970226062d1", 8)
    # 排行周
    ph_week = get_image_news("576b37cda6d2e970226062d4", 8)
    # 排行月
    ph_month = get_image_news("576b37daa6d2e970226062d7", 8)
    # 专题
    zt = search_news_db([ObjectId("5768d0b9dcc88e3891c7369c")], 5)
    # 今日热评
    jrrp = search_news_db([ObjectId("5782f547dcc88e7769576fbd")], 5)
    # 政治经济
    zzjj = search_news_db([ObjectId("5782f5cadcc88e7769576fc0")], 5)
    # 社会民生
    shms = search_news_db([ObjectId("5782f5d2dcc88e776838c3f4")], 5)
    # 文化娱乐
    whyl = search_news_db([ObjectId("5782f5dadcc88e7769576fc1")], 5)
    # 教育科技
    jykj = search_news_db([ObjectId("578311fadcc88e4cb57770c3")], 5)
    return render_template('psd/psd_index.html',
                           lht=lht,
                           ttxw=ttxw,
                           jrrp_1=jrrp_1,
                           jrrp_2=jrrp_2,
                           jrrp_5=jrrp_5,
                           djsj=djsj,
                           dszs=dszs,
                           ph_24=ph_24,
                           ph_month=ph_month,
                           ph_week=ph_week,
                           zt=zt,
                           jrrp=jrrp,
                           zzjj=zzjj,
                           shms=shms,
                           whyl=whyl,
                           jykj=jykj
                           )


# 二级频道列表
@psd_page.route('/psd/list/<channel>/')
def psd_list(channel):
    pre_page = 5
    # 轮换头图
    lht = get_head_image(ObjectId(channel), 5)
    # 新闻列表
    c_list = search_news_db([ObjectId(channel)], pre_page)
    # 今日热评文字1
    jrrp_1 = get_image_news("577c647559f0d8efacae7e68", 1)
    # 今日热评图片1
    jrrp_2 = get_image_news("577c647559f0d8efacae7e68", 1, jrrp_1)
    # 今日热评文字3
    jrrp_5 = get_image_news("577c647559f0d8efacae7e68", 3, jrrp_1 + jrrp_2)
    # 独家视界
    djsj = get_image_news("577c648559f0d8efacae7e6b", 10)
    # 当事者说
    dszs = get_image_news("577c649059f0d8efacae7e6e", 3)
    # 排行24
    ph_24 = get_image_news("576b37b8a6d2e970226062d1", 8)
    # 排行周
    ph_week = get_image_news("576b37cda6d2e970226062d4", 8)
    # 排行月
    ph_month = get_image_news("576b37daa6d2e970226062d7", 8)
    # 专题
    zt = search_news_db([ObjectId("5768d0b9dcc88e3891c7369c")], 5)
    # 频道
    detail = db.Channel.find_one({"_id": ObjectId(channel)})
    return render_template('psd/psd_list.html', lht=lht,
                           c_list=c_list,
                           jrrp_1=jrrp_1,
                           jrrp_2=jrrp_2,
                           jrrp_5=jrrp_5,
                           djsj=djsj,
                           dszs=dszs,
                           ph_24=ph_24,
                           ph_month=ph_month,
                           ph_week=ph_week,
                           zt=zt,
                           detail=detail
                           )
