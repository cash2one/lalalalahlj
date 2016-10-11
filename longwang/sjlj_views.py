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
def index():
    tt = search_indexnews_db("57faed0ab9201c3c53b0ea89", 5)
    jptj = search_indexnews_db("57faed0ab9201c3c53b0ea8a", 4)
    zxfb = search_indexnews_db("57faed0ab9201c3c53b0ea8b", 8)
    zxfb_new = list_new(zxfb)
    wqhg = search_indexnews_db("57faed0ab9201c3c53b0ea8c", 8)
    wqhg_new = list_new(wqhg)
    return render_template('sjlj/index.html', name="数据龙江",
                           tt=tt,
                           jptj=jptj,
                           zxfb=zxfb,
                           wqhg=wqhg,
                           zxfb_new=zxfb_new,
                           wqhg_new=wqhg_new
                           )


@sjlj_page.route('/sjlj/<id>.html/')
@sjlj_page.route('/sjlj/<id>_<page>.html/')
def sjlj_list(id, page=1):
    pre_page = 10
    channel = db.Channel.find_one({"numid": int(id)})
    _id = channel["_id"]
    list = search_news_db([channel["_id"]], 10)
    condition = {"Channel": {"$in": [channel["_id"]]}, "Status": 4}
    count = db.News.find(condition).sort('Pulished', pymongo.DESCENDING).count()
    news_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).skip(pre_page * (int(page) - 1)).limit(
        pre_page)
    _news_list = []
    for i in news_list:
        _news_list.append(get_mongodb_dict(i))
    pagenums, pagebar_html = pager("/sjlj/" + str(id), int(page), count, pre_page).show_page()
    return render_template('sjlj/list.html',
                           list=list,
                           channel=channel,
                           id=int(id),
                           pagebar_html=pagebar_html
                           )


def list_new(raw_list=[]):
    new_list = []
    for i in raw_list:
        raw_new = db.News.find_one({"numid": i["_id"]})
        i["ctime"] = datetime_op(raw_new["Published"])
        i["browseclick"] = raw_new["Browseclick"]
        new_list.append(i)
    return new_list
