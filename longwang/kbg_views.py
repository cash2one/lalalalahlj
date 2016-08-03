# -*- coding: utf-8 -*-#
# filename:index_news.py
# __author__ = 'wanglina'
import json
import pymongo
from flask import Blueprint, render_template
from connect import conn
from longwang.mongodb_news import search_news_db, get_head_image, image_server, datetime_op, search_indexnews_db, \
    get_mongodb_dict
from bson import ObjectId
from psd_views import get_name

db = conn.mongo_conn()
db_redis = conn.redis_conn()

kbg_page = Blueprint('kbg_page', __name__, template_folder='templates')
pre_page = 10


# 二级频道首页
@kbg_page.route('/kbg/')
def kbg_index():
    # 轮换图 4张
    lht = get_head_image(ObjectId("576500f0dcc88e31a7d2e4ba"), 5)
    # 头条新闻  15条
    tt = search_indexnews_db("577c5eaa59f0d8efacae7e4b", 15)
    # 报料台 4条
    blt1 = search_news_db([ObjectId("5782f7a4dcc88e7769576fc5")], 1, 1)
    # 报料台 4条
    blt = search_news_db([ObjectId("5782f7a4dcc88e7769576fc5")], 3, 0, blt1)
    # 龙江演出 4条
    ljyc1 = search_news_db([ObjectId("5782f81ddcc88e7769576fc8")], 2, 1)
    ljyc = search_news_db([ObjectId("5782f81ddcc88e7769576fc8")], 3, 0, ljyc1)
    # 星在龙江 4条
    xzlj1 = search_news_db([ObjectId("5782f82edcc88e776838c3fb")], 2, 1)
    xzlj = search_news_db([ObjectId("5782f82edcc88e776838c3fb")], 3, 0, xzlj1)
    # 今日要闻 10条
    jryw = search_indexnews_db("577c5ecb59f0d8efacae7e4e", 10)
    # 新闻排行
    hours = search_indexnews_db("576b37b8a6d2e970226062d1", 6)
    zb = search_indexnews_db("576b37cda6d2e970226062d4", 6)
    yb = search_indexnews_db("576b37daa6d2e970226062d7", 6)
    # 二次元 10条
    ecy = search_news_db([ObjectId("57650505dcc88e31a6f3501b")], 10)
    # 频道菜单
    menu1 = db.Channel.find({"Parent": ObjectId("576500f0dcc88e31a7d2e4ba"), "Visible": 1}).sort("OrderNumber")
    # 热专题
    zt = search_indexnews_db("577c5ee759f0d8efacae7e51", 5)
    # 明星 5带图
    mx = get_head_image(ObjectId("5765050fdcc88e31a7d2e4c3"), 5)
    # 电视 5带图
    ds = get_head_image(ObjectId("5768d0c1dcc88e3891c7369d"), 5)
    # 音乐 5带图
    yy = get_head_image(ObjectId("5768d0c9dcc88e3891c7369e"), 5)
    # 电影 1带图
    dy = get_head_image(ObjectId("5768d0b9dcc88e3891c7369c"), 1)
    # 热点影评 7
    rdyp = search_indexnews_db("57833a603c7e58bdfe540d7f", 7)
    # 本地影讯 7
    bdyx = search_indexnews_db("57833a833c7e58bdfe540d81", 7)
    # 合作媒体
    hzmt = db.Media.find({"ChannelID": ObjectId("576500f0dcc88e31a7d2e4ba")})
    # 明星 5条
    mx5 = search_news_db([ObjectId("5765050fdcc88e31a7d2e4c3")], pre_page)
    return render_template('kbg/kbg_index.html', lht=lht, tt=tt, jryw=jryw, hours=hours, zb=zb, yb=yb, blt=blt,
                           blt1=blt1, ecy=ecy,
                           ljyc=ljyc, xzlj=xzlj, ljyc1=ljyc1, xzlj1=xzlj1, menu=menu1, zt=zt, mx=mx, ds=ds, yy=yy,
                           dy=dy, rdyp=rdyp, bdyx=bdyx, hzmt=hzmt, mx5=mx5, ys="sy")


# 二级频道列表
@kbg_page.route('/kbg/<channel>/<page>/')
def kbg_list(channel, page=1):
        condition = {"Channel": {"$in": [ObjectId(channel)]}, "Status": 4}
        news_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).skip(
            pre_page * (int(page) - 1)).limit(
            pre_page)
        value = ""
        for i in news_list:
            style = 'style="display: block"'
            if i["Guideimage"] == "":
                style = 'style="display: none"'
            value += "<li><p %s><a href='/detail/%s' target='_blank'><img src='%s?w=261&h=171' width='261' height='171'/></a></p><h2><a href='/detail/%s' target='_blank'>%s</a></h2> <h5>%s</h5> <h6>&nbsp;&nbsp;&nbsp;%s</h6></li>" % \
                     (style, i["_id"], image_server + i["Guideimage"], i["_id"], i["Title"], i["Summary"],
                      datetime_op((i["Published"])))
        return json.dumps(value)


# 二级频道列表
@kbg_page.route('/kbg/list/<channel>/')
def kbg_list_index(channel):
    # 轮换图
    lht = get_head_image(ObjectId(channel), 4)
    news_list = search_news_db([ObjectId(channel)], pre_page)
    # 新闻排行
    hours = search_indexnews_db("576b37b8a6d2e970226062d1", 8)
    zb = search_indexnews_db("576b37cda6d2e970226062d4", 8)
    yb = search_indexnews_db("576b37daa6d2e970226062d7", 8)
    # 频道菜单
    menu1 = db.Channel.find({"Parent": ObjectId("576500f0dcc88e31a7d2e4ba"), "Visible": 1}).sort("OrderNumber")
    # 报料台 4条
    blt = search_news_db([ObjectId("5782f7a4dcc88e7769576fc5")], 12)
    # 热门图集
    rmtj = get_head_image(ObjectId("5768a6f4dcc88e0510fe053a"), 3)
    detail = db.Channel.find_one({"_id": ObjectId(channel)})
    return render_template('kbg/kbg_list.html', news_list=news_list, lht=lht, hours=hours, zb=zb, yb=yb,
                           cid=ObjectId(channel),
                           menu=menu1, blt=blt, rmtj=rmtj, detail=detail)
