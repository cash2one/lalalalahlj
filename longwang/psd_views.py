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

pre_page = 5


# 二级频道首页
@psd_page.route('/psd/')
def psd_index():
    # 轮换图
    lht = get_head_image(ObjectId("576500d7dcc88e31a6f3500d"), 4)
    # 头条新闻
    ttxw = get_image_news("577c646159f0d8efacae7e65", 6)
    # 今日热评文字1
    # jrrp_1 = get_image_news("577c647559f0d8efacae7e68", 1)
    # 今日热评图片1
    jrrp_2 = get_image_news("577c647559f0d8efacae7e68", 1)
    # 今日热评文字3
    jrrp_5 = get_image_news("577c647559f0d8efacae7e68", 4, jrrp_2)
    # 独家视界
    djsj = get_image_news("577c648559f0d8efacae7e6b", 10)
    # 当事者说
    dszs = get_image_news("577c649059f0d8efacae7e6e", 4)
    # 排行24
    ph_24 = get_image_news("576b37b8a6d2e970226062d1", 8)
    # 排行周
    ph_week = get_image_news("576b37cda6d2e970226062d4", 8)
    # 排行月
    ph_month = get_image_news("576b37daa6d2e970226062d7", 8)
    # 专题
    zt = search_news_db([ObjectId("5765057edcc88e31a7d2e4c6")], 5)
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
    # 合作媒体
    hzmt = db.Media.find({"ChannelID": ObjectId("576500d7dcc88e31a6f3500d")})
    menu1 = db.Channel.find({"Parent": ObjectId("576500d7dcc88e31a6f3500d"), "Visible": 1}).sort("OrderNumber")
    return render_template('psd/psd_index.html',
                           lht=lht,
                           ttxw=ttxw,
                           # jrrp_1=jrrp_1,
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
                           jykj=jykj,
                           hzmt=hzmt,
                           ys="sy",
                           menu=menu1
                           )


# 二级频道列表
@psd_page.route('/psd/')
@psd_page.route('/psd/<channel>/<page>/')
def kbg_list(channel, page=1):
    condition = {"Channel": {"$in": [ObjectId(channel)]}, "Status": 4}
    news_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).skip(pre_page * (int(page) - 1)).limit(
        pre_page)
    value = ""
    for i in news_list:
        style = 'style="display: block"'
        if i["Guideimage"] == "":
            style = 'style="display: none"'
        value += "<li><p %s><a href='/detail/%s' target='_blank'><img src='%s?w=261&h=171' width='261' height='171'/></a></p><h2><a href='/detail/%s' target='_blank'>%s</a></h2> \
        <h5>%s</h5> <h6>&nbsp;&nbsp;&nbsp;%s</h6></li>" % (
            style, i["_id"], image_server + i["Guideimage"], i["_id"], i["Title"], i["Summary"],
            datetime_op((i["Published"])))
    return json.dumps(value)


# 二级频道列表
@psd_page.route('/psd/list/<channel>/')
def psd_list(channel):
    # 轮换头图
    lht = get_head_image(ObjectId(channel), 5)
    # 新闻列表
    c_list = search_news_db([ObjectId(channel)], pre_page)
    # 今日热评文字1
    # jrrp_1 = get_image_news("577c647559f0d8efacae7e68", 1)
    # 今日热评图片1
    jrrp_2 = get_image_news("577c647559f0d8efacae7e68", 1)
    # 今日热评文字3
    jrrp_5 = get_image_news("577c647559f0d8efacae7e68", 3, jrrp_2)
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
    zt = search_news_db([ObjectId("5765057edcc88e31a7d2e4c6")], 5)
    # # 合作媒体
    # hzmt = db.Media.find({"ChannelID": ObjectId("576500f0dcc88e31a7d2e4ba")})
    # 频道
    menu1 = db.Channel.find({"Parent": ObjectId("576500d7dcc88e31a6f3500d"), "Visible": 1}).sort("OrderNumber")
    detail = db.Channel.find_one({"_id": ObjectId(channel)})
    name = get_name(channel)
    return render_template('psd/psd_list.html', lht=lht,
                           c_list=c_list,
                           # jrrp_1=jrrp_1,
                           jrrp_2=jrrp_2,
                           jrrp_5=jrrp_5,
                           djsj=djsj,
                           dszs=dszs,
                           ph_24=ph_24,
                           ph_month=ph_month,
                           ph_week=ph_week,
                           zt=zt,
                           detail=detail,
                           name=name,
                           menu=menu1,
                           cid=ObjectId(channel)
                           )


# 二级频道分页
@psd_page.route('/psd/list/<channel>/')
@psd_page.route('/psd/list/<channel>/<page>')
def news_list_page(channel, page=1):
    condition = {"Channel": {"$in": [ObjectId(channel)]}, "Status": 4}
    news_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).skip(pre_page * (int(page) - 1)).limit(
        pre_page)
    value = ""
    for i in news_list:
        style = 'style="display: block"'
        if i["Guideimage"] == "":
            style = 'style="display: none"'
        value += "<li %s><p %s><a href='/detail/%s' target='_blank'><img src='%s?w=261&h=171' width='261' height='171'/></a></p><h2><a href='/detail/%s' target='_blank'>%s</a></h2> <h5>%s</h5> <h6>&nbsp;&nbsp;&nbsp;%s</h6></li>" % \
                 (style, style, i["_id"], image_server + i["Guideimage"], i["_id"], i["Title"], i["Summary"],
                  datetime_op((i["Published"])))
    return json.dumps(value)


def get_name(channel):
    name = db.Channel.find_one({"_id": ObjectId(channel)})["Name"]
    return name
