# -*- coding: utf-8 -*-#
# filename:index_news.py
# __author__ = 'wanglina'
from longwang.pager.pager import pager
import json
import urllib2
import pymongo
from flask import Blueprint, render_template
from connect import conn
from longwang.mongodb_news import search_news_db, get_head_image, image_server, datetime_op, get_images, \
    get_mongodb_dict
from bson import ObjectId

db = conn.mongo_conn()
db_redis = conn.redis_conn()
# 侧边栏
# 专题
# zt_images = search_news_db([ObjectId("5768d0b9dcc88e3891c7369c")], 4)
# zt = search_news_db([ObjectId("5765057edcc88e31a7d2e4c6")], 3, zt_images)
zt_images = search_news_db([ObjectId("5768d0b9dcc88e3891c7369c")], 4, 1)
zt = search_news_db([ObjectId("5768d0b9dcc88e3891c7369c")], 3, 0, zt_images)
# 侃八卦
gbg = search_news_db(
    [ObjectId("576504f7dcc88e31a6f3501a"), ObjectId("57650505dcc88e31a6f3501b"), ObjectId("5765050fdcc88e31a7d2e4c3")],
    8)
# 热门图集
rmtj = search_news_db([ObjectId("5768a6f4dcc88e0510fe053a")], 9, 1, [], 2)
# 新闻排行
ph = search_news_db(
    [ObjectId("5765045adcc88e31a6f35016"), ObjectId("57650499dcc88e31a6f35018"), ObjectId("5765050fdcc88e31a7d2e4c3")],
    8)
index_page = Blueprint('index_page', __name__, template_folder='templates')

# 分页
pre_page = 9


# 首页
@index_page.route('/')
def index():
    # 轮换图
    lht = get_head_image(ObjectId("57688f50dcc88e552361ba27"), 5)
    # 要闻
    # yw = search_news_db([ObjectId("57650551dcc88e31a6f3501c")], 3)
    yw = get_images([ObjectId("5768ecd3dcc88e0c2b3bbbe6"), ObjectId("5768efccdcc88e0c2b3bbbed"),
                     ObjectId("5768f550dcc88e0c25d886d0")])
    # 高层动态
    # gcdt = search_news_db([ObjectId("576503f2dcc88e31a6f35013")], 3)
    gcdt = get_images([ObjectId("5768e960dcc88e07cb182456"), ObjectId("5768ef17dcc88e0c2b3bbbeb"),
                       ObjectId("5768f5ffdcc88e0c25d886d3")])
    # 快讯
    # kx = search_news_db([ObjectId("57650558dcc88e31a7d2e4c4")], 3)
    kx = get_images([ObjectId("5768eb0edcc88e07cb182458"), ObjectId("5768f1a5dcc88e0c2b3bbbf1"),
                     ObjectId("5768f899dcc88e0c25d886d8")])
    # 本网原创
    # bwyc = search_news_db([ObjectId("57650560dcc88e31a7d2e4c5")], 3)
    bwyc = get_images([ObjectId("5768f08bdcc88e0c2b3bbbef"), ObjectId("5768f4b0dcc88e0c2b3bbbfa"),
                       ObjectId("57690044dcc88e2870bc3d95")])
    # 首页14条新闻
    _list = search_news_db([ObjectId("576503f2dcc88e31a6f35013"), ObjectId("5765040cdcc88e31a6f35014")], 40)
    return render_template('index.html', zt_images=zt_images, zt=zt, gbg=gbg, yw=yw, gcdt=gcdt, kx=kx, bwyc=bwyc,
                           lht=lht, rmtj=rmtj, menu=get_menu(), _list=_list, ph=ph)


# 二级频道列表
@index_page.route('/list/<channel>/')
def s_list(channel):
    # 轮换图
    lht = get_head_image(ObjectId(channel), 5)
    c_list = search_news_db([ObjectId(channel)], pre_page)
    # 频道
    detail = db.Channel.find_one({"_id": ObjectId(channel)})
    return render_template('list.html', zt_images=zt_images, zt=zt, gbg=gbg, rmtj=rmtj, lht=lht, channel=c_list,
                           detail=detail, menu=get_menu(), ph=ph)


# 二级频道分页
@index_page.route('/list/<channel>/<page>')
def s_list_page(channel, page=1):
    condition = {"Channel": {"$in": [ObjectId(channel)]}, "Status": 4}
    news_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).skip(pre_page * (int(page) - 1)).limit(
        pre_page)
    value = ""
    for i in news_list:
        style = 'style="display: block"'
        if i["Guideimage"] == "":
            style = 'style="display: none"'
        value += "<li><p %s><img src='%s' width='261' height='171'/></p><h2><a href='/detail/%s' target='_blank'>%s</a></h2> <h5>%s</h5> <h6>&nbsp;&nbsp;&nbsp;%s</h6></li>" % \
                 (style, image_server + i["Guideimage"], i["_id"], i["Title"], i["Summary"],
                  datetime_op((i["Published"])))
    return json.dumps(value)


# 详细页面 分页显示
@index_page.route('/detail/<id>/')
@index_page.route('/detail/<id>/<page>/')
def detail(id, page=1):
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
    # <div style="page-break-after: always"><span style="display:none">&nbsp;</span></div>
    count = detail["Content"].split(
        '<div style="page-break-after: always"><span style="display:none">&nbsp;</span></div>')
    # print len(count)
    # for i in count:
    #     print i
    d = {}
    d["_id"] = detail["_id"]
    d["Title"] = detail["Title"]
    d["Source"] = detail["Source"]
    d["Published"] = detail["Published"]
    d["Author"] = detail["Author"]
    d["Content"] = detail["Content"]
    if len(count) > 1:
        d["Content"] = count[int(page) - 1]
    d["Editor"] = detail["Editor"]
    pagenums, pagebar_html = pager('/detail/' + str(id), int(page), len(count), 1).show_page()
    return render_template('detail.html', zt_images=zt_images, zt=zt, gbg=gbg, rmtj=rmtj, detail=d, qsmw1=qsmw1,
                           qsmw=qsmw, ssf1=ssf1, ssf=ssf, ayd1=ayd1, ayd=ayd, hrg1=hrg1, hrg=hrg, ecy1=ecy1, ecy=ecy,
                           channel=channel, menu=get_menu(), ph=ph, pagebar_html=pagebar_html, count=len(count))


# 详细页面全部显示
@index_page.route('/detail_all/<id>/')
def detail_all(id):
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
                           channel=channel, menu=get_menu(), ph=ph, count=1)


# @index_page.route('/menu/')
def get_menu():
    value = "<li class='m'><h3><a target='_blank' href='/'>首页</a></h3></li>"
    c_p = db.Channel.find(
        {"Parent": ObjectId("5428b978f639ab1548d55184"), "_id": {"$ne": ObjectId("5764f5396aba261f94bf517a")},
         "Status": 1}).sort("OrderNumber")
    for i in c_p:
        c_c = db.Channel.find({"Parent": ObjectId(i["_id"]), "Status": 1}).sort("OrderNumber")
        if c_c.count() > 0:
            value += "<li class='m'>"
            value += "<h3><a href='#'>%s</a></h3>" % (i["Name"])
            value += "<ul class='sub'>"
            for j in c_c:
                value += "<li><a href='/list/%s'>%s</a></li>" % (j["_id"], j["Name"])
            value += "</ul></li>"
        else:
            value += "<li class='m'>"
            value += "<h3><a href='/list/%s'>%s</a></h3></li>" % (i["_id"], i["Name"])

    value += "<li class='block' style='left: 167px;'></li>"
    return value


# 热词获取
@index_page.route('/get_hot/')
def search_hot_redis():
    string = ""
    count = 0
    for i in db_redis.hkeys('hot_searh'):
        if count <= 8:
            count += 1
            string += "<li><a href=\"javascript:void(0);\" onclick=\"js_method(encodeURI('%s'))\" style=\"cursor: pointer;\" target=\"_blank\">%s</a></li>" % (
                i, i)
        else:
            pass

    return json.dumps({"key": string})


# 全文搜索
@index_page.route('/ss/<keywords>/')
@index_page.route('/ss/<keywords>/<page>')
def ss_keywords(keywords, page=1):
    keyword = urllib2.unquote(str(keywords))
    k_list = db.News.find({"$text": {"$search": keyword}, "Status": 4}).sort('Published', pymongo.DESCENDING).skip(
        pre_page * (int(page) - 1)).limit(pre_page)
    c_list = []
    for i in k_list:
        c_list.append(get_mongodb_dict(i))
    return render_template('search.html', zt_images=zt_images, zt=zt, gbg=gbg, rmtj=rmtj, menu=get_menu(), ph=ph,
                           c_list=c_list, keyword=keyword)
