# coding=utf-8
from flask import Blueprint, render_template
from connect import conn
from bson import ObjectId
from longwang.mongodb_news import get_head_image, search_indexnews_db, search_news_db
import encodings

# import pymongo

klj_page = Blueprint('klj_page', __name__, template_folder='templates')
db = conn.mongo_conn()


@klj_page.route('/klj/')
def klj_index():
    name = '看龙江'
    # 轮换图
    lht = get_head_image(ObjectId("576500b1dcc88e31a7d2e4b8"), 4)
    # 二级标题列表
    menu = db.Channel.find({"Parent": ObjectId("576500b1dcc88e31a7d2e4b8"), "Visible": 1}).sort("OrderNumber")
    # 本网独家
    bwdj = search_indexnews_db("57a2aa293c7e0f7c5657ed87", 5)
    # 民情观察
    mqgc = search_indexnews_db("57a2acfd2d87e643c825a5b1", 5)
    # 地市List
    menu1 = db.Channel.find({"Parent": ObjectId("5765013ddcc88e31a7d2e4bc")}).sort("OrderNumber")
    # 城市联播
    city_list = db.IndexChannel.find({"Parent": "576500b1dcc88e31a7d2e4b8", "order": {"$ne": 0}}).sort("order")
    channel_list_id = []
    news_list = []
    city_name = []
    for i in city_list:
        channel_list_id.append(str(i["_id"]))
        news_list.append(search_indexnews_db(str(i["_id"]), 7))
    # 龙江资讯
    ljzx = search_indexnews_db("57a2b1132d87e643c825a5cf", 7)
    # 生活万象
    shwx = search_indexnews_db("57a2b1372d87e643c825a5d1", 7)
    # 图说龙江
    tslj = search_indexnews_db("57a2b1472d87e643c825a5d3", 6)
    # 领导活动报道集
    ldhdbdj = search_indexnews_db("57a2b16b2d87e643c825a5d5", 8)
    # 人事任免
    rsrm = search_news_db([ObjectId("57650161dcc88e31a6f35011")], 8)
    # 画龙点经
    hldj = search_indexnews_db("57a2b1cf2d87e643c825a5d7", 5)
    # 寒地黑土
    hdht = search_indexnews_db("57a2b2072d87e643c825a5d9", 7)
     # 专题
    zt_images = get_head_image("5765057edcc88e31a7d2e4c6", 4)
    zt = search_indexnews_db("579584633c7e431eaf791a06", 3)

    return render_template('klj/klj_index.html', name=name,
                           menu=menu,
                           lht=lht,
                           bwdj=bwdj,
                           mqgc=mqgc,
                           menu1=menu1,
                           news_list=news_list,
                           ljzx=ljzx,
                           shwx=shwx,
                           tslj=tslj,
                           ldhdbdj=ldhdbdj,
                           rsrm=rsrm,
                           hldj=hldj,
                           hdht=hdht,
                           zt_images=zt_images,
                           zt=zt
                           )
