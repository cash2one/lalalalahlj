# -*- coding: utf-8 -*-#
# filename:index_news.py
# __author__ = 'wanglina'
from longwang.pager.pager import pager
import json
import urllib2
import pymongo
from flask import Blueprint, render_template
from connect import conn
from longwang.mongodb_news import search_news_db, get_head_image, image_server, datetime_op, search_indexnews_db, \
    get_mongodb_dict
from bson import ObjectId

db = conn.mongo_conn()
db_redis = conn.redis_conn()

index_page = Blueprint('index_page', __name__, template_folder='templates')

# 分页
pre_page = 9


# 首页
@index_page.route('/')
def index():
    # 轮换图
    lht = get_head_image(ObjectId("57688f50dcc88e552361ba27"), 5)
    # 龙江头条
    yw = search_indexnews_db("576b36a9a6d2e970226062c3", 3)
    # 侃八卦
    gbg = search_indexnews_db("579190303c7ee91e3478823e", 10)
    # 专题
    zt_images = search_news_db([ObjectId("5765057edcc88e31a7d2e4c6")], 4)
    zt = search_news_db([ObjectId("5765057edcc88e31a7d2e4c6")], 3, zt_images)
    # 热门图集
    rmtj = search_news_db([ObjectId("5768a6f4dcc88e0510fe053a")], 9, 1, [], 2)
    # 今日要闻
    gcdt = search_indexnews_db("576b3715a6d2e970226062c8", 3)

    # 龙江看点
    kx = search_indexnews_db("579190303c7ee91e3478823d", 6)

    # 新闻排行
    hours = search_indexnews_db("576b37b8a6d2e970226062d1", 8)
    zb = search_indexnews_db("576b37cda6d2e970226062d4", 8)
    yb = search_indexnews_db("576b37daa6d2e970226062d7", 8)
    # 首页推荐置顶
    _list = db.IndexNews.find({"ChannelId": "579190303c7ee91e3478823f"})
    _id_list = []
    for i in _list:
        _id_list.append(ObjectId(i["NewsID"]))
    zd = db.News.find({"_id": {"$in": _id_list}})
    _zd = []
    for j in zd:
        _zd.append(get_mongodb_dict(j))
    # 首页14条新闻
    condition = {"IsSift": 1, "Guideimage": {"$ne": ""}, "Status": 4}
    news_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).limit(14)
    _news_list = []
    for news_detail in news_list:
        _news_list.append(get_mongodb_dict(news_detail))
    return render_template('index.html', zt_images=zt_images, zt=zt, gbg=gbg, yw=yw, gcdt=gcdt, kx=kx,
                           lht=lht, rmtj=rmtj, menu=get_menu(), news_list=_news_list, hours=hours, zb=zb, yb=yb, zd=_zd)


# 二级频道列表
@index_page.route('/list/<channel>/')
def s_list(channel):
    # 轮换图
    lht = get_head_image(ObjectId(channel), 5)
    c_list = search_news_db([ObjectId(channel)], pre_page)
    # 频道
    detail = db.Channel.find_one({"_id": ObjectId(channel)})
    # 新闻排行
    hours = search_indexnews_db("576b37b8a6d2e970226062d1", 8)
    zb = search_indexnews_db("576b37cda6d2e970226062d4", 8)
    yb = search_indexnews_db("576b37daa6d2e970226062d7", 8)
    # 侃八卦
    gbg = search_indexnews_db("579190303c7ee91e3478823e", 10)
    # 专题
    zt_images = search_news_db([ObjectId("5765057edcc88e31a7d2e4c6")], 4)
    zt = search_news_db([ObjectId("5765057edcc88e31a7d2e4c6")], 3, zt_images)
    # 热门图集
    rmtj = search_news_db([ObjectId("5768a6f4dcc88e0510fe053a")], 9, 1, [], 2)
    return render_template('list.html', zt_images=zt_images, zt=zt, gbg=gbg, rmtj=rmtj, lht=lht, channel=c_list,
                           detail=detail, menu=get_menu(), hours=hours, zb=zb, yb=yb)


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
    ayd1 = search_news_db([ObjectId("5782ffcbdcc88e128e6cd34e")], 1)
    ayd = search_news_db([ObjectId("5782ffcbdcc88e128e6cd34e")], 8, ayd1)
    # 红人馆
    # hrg1 = search_news_db([ObjectId("576504f7dcc88e31a6f3501a")], 1)
    # hrg = search_news_db([ObjectId("576504f7dcc88e31a6f3501a")], 8, hrg1)
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
    # 新闻排行
    hours = search_indexnews_db("576b37b8a6d2e970226062d1", 8)
    zb = search_indexnews_db("576b37cda6d2e970226062d4", 8)
    yb = search_indexnews_db("576b37daa6d2e970226062d7", 8)
    pagenums, pagebar_html = pager('/detail/' + str(id), int(page), len(count), 1).show_page()
    # 侃八卦
    gbg = search_indexnews_db("579190303c7ee91e3478823e", 10)
    # 专题
    zt_images = search_news_db([ObjectId("5765057edcc88e31a7d2e4c6")], 4)
    zt = search_news_db([ObjectId("5765057edcc88e31a7d2e4c6")], 3, zt_images)
    # 热门图集
    rmtj = search_news_db([ObjectId("5768a6f4dcc88e0510fe053a")], 9, 1, [], 2)
    return render_template('detail.html', zt_images=zt_images, zt=zt, gbg=gbg, rmtj=rmtj, detail=d, qsmw1=qsmw1,
                           qsmw=qsmw, ssf1=ssf1, ssf=ssf, ayd1=ayd1, ayd=ayd, ecy1=ecy1, ecy=ecy,
                           channel=channel, menu=get_menu(), hours=hours, zb=zb, yb=yb, pagebar_html=pagebar_html,
                           count=len(count))


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
    # 新闻排行
    hours = search_indexnews_db("576b37b8a6d2e970226062d1", 8)
    zb = search_indexnews_db("576b37cda6d2e970226062d4", 8)
    yb = search_indexnews_db("576b37daa6d2e970226062d7", 8)
    # 侃八卦
    gbg = search_indexnews_db("579190303c7ee91e3478823e", 10)
    # 专题
    zt_images = search_news_db([ObjectId("5765057edcc88e31a7d2e4c6")], 4)
    zt = search_news_db([ObjectId("5765057edcc88e31a7d2e4c6")], 3, zt_images)
    # 热门图集
    rmtj = search_news_db([ObjectId("5768a6f4dcc88e0510fe053a")], 9, 1, [], 2)
    return render_template('detail.html', zt_images=zt_images, zt=zt, gbg=gbg, rmtj=rmtj, detail=detail, qsmw1=qsmw1,
                           qsmw=qsmw, ssf1=ssf1, ssf=ssf, ayd1=ayd1, ayd=ayd, hrg1=hrg1, hrg=hrg, ecy1=ecy1, ecy=ecy,
                           channel=channel, menu=get_menu(), hours=hours, zb=zb, yb=yb, count=1)


# @index_page.route('/menu/')
def get_menu():
    value = "<li class='m'><h3><a target='_blank' href='/'>首页</a></h3></li>"
    c_p = db.Channel.find(
        {"Parent": ObjectId("5428b978f639ab1548d55184"), "_id": {"$ne": ObjectId("5764f5396aba261f94bf517a")},
         "Status": 1, "Visible": 1}).sort("OrderNumber")
    for i in c_p:
        c_c = db.Channel.find({"Parent": ObjectId(i["_id"]), "Status": 1, "Visible": 1}).sort("OrderNumber")
        if c_c.count() > 0:
            value += "<li class='m'>"
            value += "<h3><a href='%s'>%s</a></h3>" % (i["Href"], i["Name"])
            value += "<ul class='sub'>"
            for j in c_c:
                value += "<li><a href='%s'>%s</a></li>" % (j["Href"], j["Name"])
            value += "</ul></li>"
        else:
            value += "<li class='m'>"
            value += "<h3><a href='%s'>%s</a></h3></li>" % (i["Href"], i["Name"])
    value += "<li class='block' style='left: 167px;'></li>"
    return value


def set_menu():
    c_p = db.Channel.find(
        {"Parent": ObjectId("5428b978f639ab1548d55184"), "_id": {"$ne": ObjectId("5764f5396aba261f94bf517a")},
         "Status": 1}).sort("OrderNumber")
    for i in c_p:
        c_c = db.Channel.find({"Parent": ObjectId(i["_id"]), "Status": 1}).sort("OrderNumber")
        if c_c.count() > 0:
            for j in c_c:
                db.Channel.update({"_id": j["_id"]}, {"$set": {"Href": "/list/" + str(j["_id"])}})
        else:
            db.Channel.update({"_id": i["_id"]}, {"$set": {"Href": "/list/" + str(i["_id"])}})
    return "success"


# 热词获取
@index_page.route('/get_hot/')
def search_hot_redis():
    string = ""
    count = 0
    for i in db_redis.hkeys('hot_searh'):
        if len(i) < 24:
            if count <= 8:
                count += 1
                string += "<li><a href=\"javascript:void(0);\" onclick=\"js_method(encodeURI('%s'))\" style=\"cursor: pointer;\" target=\"_blank\">%s</a></li>" % (
                    i, i)
            else:
                pass
        else:
            pass
    return json.dumps({"key": string})


# 全文搜索
@index_page.route('/ss/<keywords>/')
@index_page.route('/ss/<keywords>/<page>')
def ss_keywords(keywords, page=1):
    keyword = urllib2.unquote(str(keywords))
    # condition={"$or": [{"$text": {"$search": keyword}}, {"title": {"$regex": keyword}}]}
    condition = {"$text": {"$search": keyword}, "Status": 4}
    k_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).skip(
        pre_page * (int(page) - 1)).limit(pre_page)
    c_list = []
    for i in k_list:
        c_list.append(get_mongodb_dict(i))
    # 新闻排行
    hours = search_indexnews_db("576b37b8a6d2e970226062d1", 8)
    zb = search_indexnews_db("576b37cda6d2e970226062d4", 8)
    yb = search_indexnews_db("576b37daa6d2e970226062d7", 8)
    # 侃八卦
    gbg = search_indexnews_db("579190303c7ee91e3478823e", 10)
    # 专题
    zt_images = search_news_db([ObjectId("5765057edcc88e31a7d2e4c6")], 4)
    zt = search_news_db([ObjectId("5765057edcc88e31a7d2e4c6")], 3, zt_images)
    # 热门图集
    rmtj = search_news_db([ObjectId("5768a6f4dcc88e0510fe053a")], 9, 1, [], 2)
    return render_template('search.html', zt_images=zt_images, zt=zt, gbg=gbg, rmtj=rmtj, menu=get_menu(), hours=hours,
                           zb=zb, yb=yb,
                           c_list=c_list, keyword=keyword)


# 首页下拉
@index_page.route('/issift/<page>/')
def is_sift(page=1):
    condition = {"IsSift": 1, "Guideimage": {"$ne": ""}, "Status": 4}
    news_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).skip((int(page) - 1) * 14).limit(14)
    string = ""
    for i in news_list:
        string += "<li><p><a href='/detail/%s' target='_blank'>" % (i["_id"])
        string += "<img src='%s?w=261&h=171, width='261' height='171'/></a></p><h3 class='Txt_cu'><a href='/detail/%s' target='_blank'>%s</a></h3>" % (
            image_server + i["Guideimage"], i["_id"], i["Title"])
        string += "<h4>%s</h4><span><h5>%s</h5>" % (i["Summary"], datetime_op(i["Published"]))
        c = db.Channel.find_one({"_id": ObjectId(i["Channel"][0])})
        string += "<h6><a href='%s'>%s</a></h6></span></li>" % (c["Href"], c["Name"])
    return json.dumps({"datalist": string})
