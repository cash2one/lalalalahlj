# encoding:utf-8
import json

import datetime
import pymongo
import urllib2
from flask import Blueprint, render_template, redirect
from connect import conn
from longwang.mongodb_news import search_news_db, get_head_image, image_server, datetime_op, search_indexnews_db, \
    get_mongodb_dict, get_image_news, ym_server
from bson import ObjectId

db = conn.mongo_conn()

wap_page = Blueprint('wap_page', __name__, template_folder='templates')
zd = []  # 存放专题
pre_page = 10


# 首页
@wap_page.route("/m/")
def m_index():
    # 轮换图3张
    lht = get_head_image(ObjectId("57688f50dcc88e552361ba27"), 5)
    # 首页推荐置顶
    _list = db.IndexNews.find({"ChannelId": "579190303c7ee91e3478823f"}).sort("orderno", pymongo.ASCENDING)
    tjzd = []
    for i in _list:
        zd.append(i["NewsID"])
        news = db.News.find_one({"_id": ObjectId(i["NewsID"])})
        tjzd.append(news)
    # 首页10条新闻
    condition = {"IsSift": 1, "Guideimage": {"$ne": ""}, "_id": {"$nin": zd}, "Status": 4}
    news_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).limit(pre_page)
    for news_detail in news_list:
        zd.append(i["_id"])
        tjzd.append(news_detail)
    return render_template("wap_site/index.html", lht=lht, tjzd=tjzd)


# 二级列表
@wap_page.route("/m/list<cid>")
def m_list(cid):
    channel_raw = db.Channel.find_one({"numid": int(cid)})
    child = db.Channel.find({"Parent": ObjectId(channel_raw["_id"]), "Visible": 1}).sort("OrderNumber")
    idlist = []
    for i in child:
        idlist.append(ObjectId(i["_id"]))
    condition = {"Channel": {"$in": idlist}, "Status": 4}
    news = db.News.find(condition).sort('Published', pymongo.DESCENDING).limit(pre_page)
    print news.count()
    return render_template("wap_site/list.html", channel_raw=channel_raw, news=news)


# 二级列表下拉
@wap_page.route("/m/list_<cid>_<page>")
def m_list_by_id(cid, page=1):
    channel_raw = db.Channel.find_one({"numid": int(cid)})
    child = db.Channel.find({"Parent": ObjectId(channel_raw["_id"]), "Visible": 1}).sort("OrderNumber")
    idlist = []
    for i in child:
        idlist.append(i["_id"])
    condition = {"Channel": {"$in": idlist}, "Status": 4}
    news_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).skip((int(page) - 1) * pre_page).limit(
        pre_page)
    string = ""
    for i in news_list:
        string += "<li><a href='/d/%s.html'>" % (i["numid"])
        if i["Guideimage"] != "":
            string += "<img src='%s' class='news-img' />" % (image_server + i["Guideimage"])
        string += "<div class='m_article_desc_l'>%s</div>" % (datetime_op(i["Published"]))
        string += "<div class='news-text'><h3>%s</h3></div>" % (i["Title"])
        string += "</a></li>"
    return json.dumps(string)


# 首页下拉
@wap_page.route('/m_index/<page>/')
def m_index_page(page=1):
    condition = {"IsSift": 1, "Guideimage": {"$ne": ""}, "_id": {"$nin": zd}, "Status": 4}
    news_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).skip((int(page) - 1) * pre_page).limit(
        pre_page)
    string = ""
    for i in news_list:
        string += "<li><a href='/d/%s.html'>" % (i["numid"])
        if i["Guideimage"] != "":
            string += "<img src='%s' class='news-img' />" % (image_server + i["Guideimage"])
        string += "<div class='m_article_desc_l'>%s</div>" % (datetime_op(i["Published"]))
        string += "<div class='news-text'><h3>%s</h3></div>" % (i["Title"])
        string += "</a></li>"
    return json.dumps(string)


# 新闻详细
@wap_page.route("/m/d/<id>.html")
def m_detail(id):
    detail = db.News.find_one({"numid": int(id)})
    parent_id = detail["channelnumid"][0]
    gparent_id = db.Channel.find_one({"numid": int(parent_id)})["Parent"]
    gparent_name = db.Channel.find_one({"_id":ObjectId(gparent_id)})["Name"]
    if detail["newstype"] == 2:
        return render_template("wap_site/photo-end.html", detail=detail, gparent_name=gparent_name)
    if detail["newstype"] == 3:
        zt = db.File_upload.find_one({"newsid": id, "index": 1})
        if zt is None:
            return render_template("404.html")
        else:
            return redirect(ym_server + str(zt["url"]))
    return render_template("wap_site/end.html", detail=detail, gparent_name=gparent_name)


# 龙江搜索
@wap_page.route("/m/ss/")
def m_ss():
    return render_template("wap_site/seach.html")


# 龙网搜索
@wap_page.route("/m/ss_<keys>_<page>")
def ss_keys_page(keys, page=1):
    keyword = urllib2.unquote(str(keys))
    condition = {"Status": 4}
    condition.update(
        {"$or": [{"Title": {"$regex": keyword}}, {"Content": {"regex": keyword}}, {"Keywords": {"$in": [keyword]}}]})
    news_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).skip((int(page) - 1) * pre_page).limit(
        pre_page)
    string = ""
    for i in news_list:
        string += "<li><a href='/d/%s.html'>" % (i["numid"])
        if i["Guideimage"] != "":
            string += "<img src='%s' class='news-img' />" % (image_server + i["Guideimage"])
        string += "<div class='m_article_desc_l'>%s</div>" % (datetime_op(i["Published"]))
        string += "<div class='news-text'><h3>%s</h3></div>" % (i["Title"])
        string += "</a></li>"
    return json.dumps(string)


# 自定义过滤器 图片加域名
@wap_page.app_template_filter('img_dom')
def img_dom(url):
    return image_server + url


# 自定义过滤器 时间过滤器
@wap_page.app_template_filter('time_filter')
def datetime_op(date_time):
    now = datetime.datetime.now()
    passed = now - date_time
    year = passed.days / 365
    month = passed.days / 30
    day = passed.days
    hour = passed.seconds / 3600
    minute = passed.seconds / 60
    if year > 0:
        return '{0}年前'.format(year)
    if month > 0:
        return '{0}月前'.format(month)
    if day > 0:
        return '{0}天前'.format(day)
    if hour > 0:
        return '{0}小时前'.format(hour)
    if minute > 0:
        return '{0}分钟前'.format(minute)
    if passed.seconds < 60:
        return '刚刚'
    return str(date_time)
