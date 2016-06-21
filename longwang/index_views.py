# -*- coding: utf-8 -*-#
# filename:index_news.py
# __author__ = 'wanglina'
import json

import pymongo
from flask import Blueprint, render_template
from connect import conn
from longwang.mongodb_news import search_news_db, get_head_image, image_server, switch_string_to_time
from bson import ObjectId

db = conn.mongo_conn()

# 侧边栏
# 专题
zt_images = search_news_db([ObjectId("5765057edcc88e31a7d2e4c6")], 4)
zt = search_news_db([ObjectId("5765057edcc88e31a7d2e4c6")], 3, zt_images)
# 侃八卦
gbg = search_news_db(
    [ObjectId("576504f7dcc88e31a6f3501a"), ObjectId("57650505dcc88e31a6f3501b"), ObjectId("5765050fdcc88e31a7d2e4c3")],
    10)
# 热门图集
rmtj = search_news_db([ObjectId("5768a6f4dcc88e0510fe053a")], 9, [], 2)
index_page = Blueprint('index_page', __name__, template_folder='templates')


@index_page.route('/')
def index():
    # 轮换图
    lht = get_head_image(ObjectId("57688f50dcc88e552361ba27"), 5)
    # 要闻
    yw = search_news_db([ObjectId("57650551dcc88e31a6f3501c")], 3)
    # 高层动态
    gcdt = search_news_db([ObjectId("576503f2dcc88e31a6f35013")], 3)
    # 快讯
    kx = search_news_db([ObjectId("57650558dcc88e31a7d2e4c4")], 3)
    # 本网原创
    bwyc = search_news_db([ObjectId("57650560dcc88e31a7d2e4c5")], 3)
    return render_template('index.html', zt_images=zt_images, zt=zt, gbg=gbg, yw=yw, gcdt=gcdt, kx=kx, bwyc=bwyc,
                           lht=lht, rmtj=rmtj, menu=get_menu())


@index_page.route('/list/<channel>/')
def s_list(channel):
    # 轮换图
    lht = get_head_image(ObjectId(channel), 5)
    c_list = search_news_db([ObjectId(channel)], 5)
    # 频道
    detail = db.Channel.find_one({"_id": ObjectId(channel)})
    return render_template('list.html', zt_images=zt_images, zt=zt, gbg=gbg, rmtj=rmtj, lht=lht, channel=c_list,
                           detail=detail, menu=get_menu())


@index_page.route('/list/<channel>/<page>')
def s_list_page(channel, page=1):
    pre_page = 5
    condition = {"Channel": {"$in": [ObjectId(channel)]}, "Status": 4}
    news_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).skip(pre_page * (int(page) - 1)).limit(
        pre_page)
    _list = []
    value=""
    for i in news_list:
      value=value+" <li><p><img src='%s' width='261' height='171'/></p><h2><a href='/detail/%s' target='_blank'>%s</a></h2> <h5>%s</h5> <h6>&nbsp;&nbsp;&nbsp;%s</h6></li>" %\
                  (image_server + i["Guideimage"], i["_id"],i["Title"],i["Summary"],switch_string_to_time(str(i["Published"])))
    return json.dumps(value)


@index_page.route('/detail/<id>/')
def detail(id):
    # 新闻详细
    detail = db.News.find_one({"_id": ObjectId(id)})
    # 频道
    channel = db.Channel.find_one({"_id": ObjectId(detail["Channel"][0])})
    # 趣事秒闻
    qsmw1 = search_news_db([ObjectId("57650479dcc88e31a6f35017")], 1)
    qsmw = search_news_db([ObjectId("57650479dcc88e31a6f35017")], 8, qsmw1)
    # 时尚范
    ssf1 = search_news_db([ObjectId("576504bddcc88e31a6f35019")], 1)
    ssf = search_news_db([ObjectId("576504bddcc88e31a6f35019")], 8, ssf1)
    # 爱运动
    ayd1 = search_news_db([ObjectId("576504cddcc88e31a7d2e4c2")], 1)
    ayd = search_news_db([ObjectId("576504cddcc88e31a7d2e4c2")], 8, ayd1)
    # 红人馆
    hrg1 = search_news_db([ObjectId("576504f7dcc88e31a6f3501a")], 1)
    hrg = search_news_db([ObjectId("576504f7dcc88e31a6f3501a")], 8, hrg1)
    # 二次元
    ecy1 = search_news_db([ObjectId("57650505dcc88e31a6f3501b")], 1)
    ecy = search_news_db([ObjectId("57650505dcc88e31a6f3501b")], 8, ecy1)
    return render_template('detail.html', zt_images=zt_images, zt=zt, gbg=gbg, rmtj=rmtj, detail=detail, qsmw1=qsmw1,
                           qsmw=qsmw, ssf1=ssf1, ssf=ssf, ayd1=ayd1, ayd=ayd, hrg1=hrg1, hrg=hrg, ecy1=ecy1, ecy=ecy,
                           channel=channel, menu=get_menu())


# @index_page.route('/menu/')
def get_menu():
    value = "<li class='m'><h3><a target='_blank' href='/'>首页</a></h3></li>"
    c_p = db.Channel.find(
        {"Parent": ObjectId("5428b978f639ab1548d55184"), "_id": {"$ne": ObjectId("5764f5396aba261f94bf517a")},
         "Status": 1}).sort("OrderNumber")
    for i in c_p:
        c_c = db.Channel.find({"Parent": ObjectId(i["_id"]), "Status": 1}).sort("OrderNumber")
        if c_c.count() > 0:
            value = value + "<li class='m'>"
            value = value + "<h3><a target='_blank' href='#'>%s</a></h3>" % (i["Name"])
            value = value + "<ul class='sub'>"
            for j in c_c:
                value = value + "<li><a href='/list/%s'>%s</a></li>" % (j["_id"], j["Name"])
            value = value + "</ul></li>"
        else:
            value = value + "<li class='m'>"
            value = value + "<h3><a target='_blank' href='/list/%s'>%s</a></h3></li>" % (i["_id"], i["Name"])

    value = value + "<li class='block' style='left: 167px;'></li>"
    return value
