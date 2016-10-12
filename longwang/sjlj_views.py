# coding=utf-8

import pymongo
from connect import conn
from flask import Blueprint, Flask, render_template
from mongodb_news import search_indexnews_db, search_news_db, get_mongodb_dict, datetime_op
from bson import ObjectId
from longwang.pager.pager import pager

db = conn.mongo_conn()
sjlj_page = Blueprint('sjlj_page', __name__, template_folder="templates")


@sjlj_page.route("/sjlj/")
def index():  # 数据龙江首页
    # 头图 5条
    tt = search_indexnews_db("57faed0ab9201c3c53b0ea89", 5)
    # 精品推荐 4条
    jptj = search_indexnews_db("57faed0ab9201c3c53b0ea8a", 4)
    # 最新发布 8条
    zxfb = search_indexnews_db("57faed0ab9201c3c53b0ea8b", 8)
    # 增加点击次数和日期
    zxfb_new = list_new(zxfb)
    # 往期回顾 8条
    wqhg = search_indexnews_db("57faed0ab9201c3c53b0ea8c", 8)
    # 增加点击次数和日期
    wqhg_new = list_new(wqhg)
    return render_template('sjlj/index.html', name="数据龙江",
                           tt=tt,
                           jptj=jptj,
                           zxfb=zxfb,
                           wqhg=wqhg,
                           zxfb_new=zxfb_new,
                           wqhg_new=wqhg_new
                           )


@sjlj_page.route('/sjlj/<id>.html')
@sjlj_page.route('/sjlj/<id>_<page>.html')
def sjlj_list(id, page=1):   # 数据龙江列表页
    pre_page = 10  # 当前页最多新闻条数
    channel = db.Channel.find_one({"numid": int(id)})  #频道内容
    # _id = channel["_id"]
    list = search_news_db([channel["_id"]], 10)
    condition = {"Channel": {"$in": [channel["_id"]]}, "Status": 4}
    # 翻页内容
    count = db.News.find(condition).sort('Pulished', pymongo.DESCENDING).count()
    news_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).skip(pre_page * (int(page) - 1)).limit(
        pre_page)
    _news_list = []
    for i in news_list:
        _news_list.append(get_mongodb_dict(i))
    pagenums, pagebar_html = pager("/sjlj/" + str(id), int(page), count, pre_page).show_page()
    return render_template('sjlj/list.html',
                           # list=list,
                           channel=channel,
                           _news_list=_news_list,
                           id=int(id),
                           pagebar_html=pagebar_html
                           )


def list_new(raw_list=[]):
    # 在indexnews内容里增加发布时间和点击次数两项内容
    new_list = []
    for i in raw_list:
        raw_new = db.News.find_one({"numid": i["_id"]})
        i["ctime"] = str(raw_new["Published"])[0:10]
        i["browseclick"] = raw_new["Browseclick"]
        new_list.append(i)
    return new_list
