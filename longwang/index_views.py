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
pre_page = 10
zd = []


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
    zt_images = get_head_image("5765057edcc88e31a7d2e4c6", 4)
    zt = search_indexnews_db("579584633c7e431eaf791a06", 3)
    # 热门图集
    rmtj = get_head_image(ObjectId("5768a6f4dcc88e0510fe053a"), 3)
    # 今日要闻
    gcdt = search_indexnews_db("576b3715a6d2e970226062c8", 4)
    # 龙江看点
    ljkd = search_indexnews_db("579190303c7ee91e3478823d", 5)
    # 新闻排行
    hours = search_indexnews_db("576b37b8a6d2e970226062d1", 8)
    zb = search_indexnews_db("576b37cda6d2e970226062d4", 8)
    yb = search_indexnews_db("576b37daa6d2e970226062d7", 8)
    # 首页推荐置顶
    _list = db.IndexNews.find({"ChannelId": "579190303c7ee91e3478823f"})
    _id_list = []
    for i in _list:
        _id_list.append(ObjectId(i["NewsID"]))
    zd = _id_list
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
    return render_template('index.html', zt_images=zt_images, zt=zt, gbg=gbg, yw=yw, gcdt=gcdt, ljkd=ljkd, lht=lht,
                           rmtj=rmtj,
                           menu=get_menu(),
                           news_list=_news_list,
                           hours=hours, zb=zb, yb=yb, zd=_zd)


# 二级频道列表
@index_page.route('/list/<id>/')
def s_list(id):
    channel = db.Channel.find_one({"numid": int(id)})["_id"]
    # 轮换图
    lht = get_head_image(ObjectId(channel), 5)
    c_list = search_news_db([ObjectId(channel)], pre_page)
    # 频道
    detail = db.Channel.find_one({"numid": int(id)})
    # 新闻排行
    hours = search_indexnews_db("576b37b8a6d2e970226062d1", 8)
    zb = search_indexnews_db("576b37cda6d2e970226062d4", 8)
    yb = search_indexnews_db("576b37daa6d2e970226062d7", 8)
    # 侃八卦
    gbg = search_indexnews_db("579190303c7ee91e3478823e", 10)
    # 专题
    zt_images = get_head_image("5765057edcc88e31a7d2e4c6", 4)
    zt = search_indexnews_db("579584633c7e431eaf791a06", 3)
    # 热门图集
    rmtj = get_head_image(ObjectId("5768a6f4dcc88e0510fe053a"), 3)
    return render_template('list.html', zt_images=zt_images, zt=zt, gbg=gbg, rmtj=rmtj, lht=lht, channel=c_list,
                           detail=detail, menu=get_menu(), hours=hours, zb=zb, yb=yb)


# 二级频道分页
@index_page.route('/list/<id>/<page>')
def s_list_page(id, page=1):
    channel = db.Channel.find_one({"numid": int(id)})["_id"]
    condition = {"Channel": {"$in": [ObjectId(channel)]}, "Status": 4}
    news_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).skip(pre_page * (int(page) - 1)).limit(
        pre_page)
    value = ""
    for i in news_list:
        style = 'style="display: block"'
        if i["Guideimage"] == "":
            style = 'style="display: none"'
        value += "<li><p %s><img src='%s' width='261' height='171'/></p><h2><a href='/detail/%s' target='_blank'>%s</a></h2> <h5>%s</h5> <h6>&nbsp;&nbsp;&nbsp;%s</h6></li>" % \
                 (style, image_server + i["Guideimage"], i["numid"], i["Title"], i["Summary"],
                  datetime_op((i["Published"])))
    return json.dumps(value)


# 详细页面 分页显示
@index_page.route('/detail/<id>/')
@index_page.route('/detail/<id>/<page>/')
def detail(id, page=1):
    # 新闻详细
    detail = db.News.find_one({"numid": int(id)})
    if detail["newstype"] == 2:
        # wqhg = db.News.find(
        #     {"Channel": {"$in": detail["Channel"]}, "Published": {"$gt": detail["Published"]}, "Status": 4,
        #      "Guideimage": {"$ne": ""}}).sort(
        #     "Published", pymongo.DESCENDING).limit(20)
        wqhg = db.News.find(
            {"Published": {"$gt": detail["Published"]}, "Status": 4,
             "Guideimage": {"$ne": ""}}).sort(
            "Published", pymongo.DESCENDING).limit(20)
        return render_template('picview.html', detail=detail, wqhg=wqhg)
    # 频道
    channel = db.Channel.find_one({"_id": ObjectId(detail["Channel"][0])})
    # 趣事秒闻
    # qsmw1 = search_news_db([ObjectId("57650479dcc88e31a6f35017")], 1)
    qsmw = search_news_db([ObjectId("57650479dcc88e31a6f35017")], 6, 1)
    # 时尚范
    # ssf1 = search_news_db([ObjectId("576504bddcc88e31a6f35019")], 1)
    ssf = search_news_db([ObjectId("576504bddcc88e31a6f35019")], 6, 1)
    # 爱运动
    # ayd1 = search_news_db([ObjectId("5782ffcbdcc88e128e6cd34e")], 1)
    ayd = search_news_db([ObjectId("5782ffcbdcc88e128e6cd34e")], 6, 1)
    # 红人馆
    # hrg1 = search_news_db([ObjectId("576504f7dcc88e31a6f3501a")], 1)
    hrg = search_news_db([ObjectId("576504f7dcc88e31a6f3501a")], 6, 1)
    # 二次元
    # ecy1 = search_news_db([ObjectId("57650505dcc88e31a6f3501b")], 1)
    ecy = search_news_db([ObjectId("57650505dcc88e31a6f3501b")], 6, 1)
    # <div style="page-break-after: always"><span style="display:none">&nbsp;</span></div>
    count = detail["Content"].split(
        '<div style="page-break-after: always"><span style="display:none">&nbsp;</span></div>')
    # print len(count)
    # for i in count:
    #     print i
    d = {}
    d["_id"] = detail["numid"]
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
    zt_images = get_head_image("5765057edcc88e31a7d2e4c6", 4)
    zt = search_indexnews_db("579584633c7e431eaf791a06", 3)
    # 热门图集
    rmtj = get_head_image(ObjectId("5768a6f4dcc88e0510fe053a"), 3)
    # 热门推荐
    rmtui = search_indexnews_db("579716ec3c7e62e2dacb8f75", 5)
    return render_template('detail.html', zt_images=zt_images, zt=zt, gbg=gbg, rmtj=rmtj, detail=d,
                           qsmw=qsmw, ssf=ssf, ayd=ayd, ecy=ecy,
                           channel=channel, menu=get_menu(), hours=hours, zb=zb, yb=yb, pagebar_html=pagebar_html,
                           count=len(count), rmtui=rmtui, d=1)


# 详细页面全部显示
@index_page.route('/detail_all/<id>/')
def detail_all(id):
    # 新闻详细
    detail = db.News.find_one({"numid": int(id)})
    # 频道
    channel = db.Channel.find_one({"_id": ObjectId(detail["Channel"][0])})
    # 趣事秒闻
    qsmw1 = search_news_db([ObjectId("57650479dcc88e31a6f35017")], 1)
    qsmw = search_news_db([ObjectId("57650479dcc88e31a6f35017")], 6, qsmw1)
    # 时尚范
    ssf1 = search_news_db([ObjectId("576504bddcc88e31a6f35019")], 1)
    ssf = search_news_db([ObjectId("576504bddcc88e31a6f35019")], 6, ssf1)
    # 爱运动
    ayd1 = search_news_db([ObjectId("5782ffcbdcc88e128e6cd34e")], 1)
    ayd = search_news_db([ObjectId("5782ffcbdcc88e128e6cd34e")], 6, ayd1)
    # 红人馆
    hrg1 = search_news_db([ObjectId("576504f7dcc88e31a6f3501a")], 1)
    hrg = search_news_db([ObjectId("576504f7dcc88e31a6f3501a")], 6, hrg1)
    # 二次元
    ecy1 = search_news_db([ObjectId("57650505dcc88e31a6f3501b")], 1)
    ecy = search_news_db([ObjectId("57650505dcc88e31a6f3501b")], 6, ecy1)
    # 新闻排行
    hours = search_indexnews_db("576b37b8a6d2e970226062d1", 8)
    zb = search_indexnews_db("576b37cda6d2e970226062d4", 8)
    yb = search_indexnews_db("576b37daa6d2e970226062d7", 8)
    # 侃八卦
    gbg = search_indexnews_db("579190303c7ee91e3478823e", 10)
    # 专题
    zt_images = get_head_image("5765057edcc88e31a7d2e4c6", 4)
    zt = search_indexnews_db("579584633c7e431eaf791a06", 3)
    # 热门图集
    rmtj = get_head_image(ObjectId("5768a6f4dcc88e0510fe053a"), 3)
    # 热门推荐
    rmtui = search_indexnews_db("579716ec3c7e62e2dacb8f75", 5)
    return render_template('detail.html', zt_images=zt_images, zt=zt, gbg=gbg, rmtj=rmtj, detail=detail, qsmw1=qsmw1,
                           qsmw=qsmw, ssf1=ssf1, ssf=ssf, ayd1=ayd1, ayd=ayd, hrg1=hrg1, hrg=hrg, ecy1=ecy1, ecy=ecy,
                           channel=channel, menu=get_menu(), hours=hours, zb=zb, yb=yb, count=1, rmtui=rmtui, d=1)


# @index_page.route('/menu/')
def get_menu():
    value = "<li class='m'><h3><a href='/'>首页</a></h3></li>"
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
    object_list = db_redis.lrange('hot_list', 0, 200)
    for i in object_list:
        i = str(i).replace('\n', '').replace('\r', '')
        detail = eval(i)
        if len(detail["title"]) < 24:
            if count <= 8:
                count += 1
                string += "<li><a href=\"javascript:void(0);\" onclick=\"js_method(encodeURI('%s'))\" style=\"cursor: pointer;\" target=\"_blank\">%s</a></li>" % (
                    detail["title"], detail["title"])
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
    zt_images = get_head_image("5765057edcc88e31a7d2e4c6", 4)
    zt = search_indexnews_db("579584633c7e431eaf791a06", 3)
    # 热门图集
    rmtj = get_head_image(ObjectId("5768a6f4dcc88e0510fe053a"), 3)
    return render_template('search.html', zt_images=zt_images, zt=zt, gbg=gbg, rmtj=rmtj, menu=get_menu(), hours=hours,
                           zb=zb, yb=yb,
                           c_list=c_list, keyword=keyword)


# 首页下拉
@index_page.route('/issift/<page>/')
def is_sift(page=1):
    condition = {"IsSift": 1, "Guideimage": {"$ne": ""}, "Status": 4, "_id": {"$nin": zd}}
    news_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).skip((int(page) - 1) * 14).limit(14)
    string = ""
    for i in news_list:
        string += "<li><p><a href='/detail/%s' target='_blank'>" % (i["numid"])
        string += "<img src='%s?w=261&h=171, width='261' height='171'/></a></p><h3 class='Txt_cu'><a href='/detail/%s' target='_blank'>%s</a></h3>" % (
            image_server + i["Guideimage"], i["numid"], i["Title"])
        string += "<h4>%s</h4><span><h5>%s</h5>" % (i["Summary"], datetime_op(i["Published"]))
        c = db.Channel.find_one({"_id": ObjectId(i["Channel"][0])})
        string += "<h6><a href='%s'>%s</a></h6></span></li>" % (c["Href"], c["Name"])
    return json.dumps({"datalist": string})


# 一级页面首页（除侃八卦和品深度）

@index_page.route('/fllist/<id>/')
def front_page(id):
    channel = db.Channel.find_one({"numid": int(id)})["_id"]
    lht = get_head_image(channel, 5)
    channel_list_raw = db.Channel.find({"Parent": ObjectId(channel)})
    channel_list = []
    for i in channel_list_raw:
        channel_list.append(i["_id"])
    news_list = search_news_db(channel_list, 9, 1)
    detail = db.Channel.find_one({"_id": ObjectId(channel)})
    # 新闻排行
    hours = search_indexnews_db("576b37b8a6d2e970226062d1", 8)
    zb = search_indexnews_db("576b37cda6d2e970226062d4", 8)
    yb = search_indexnews_db("576b37daa6d2e970226062d7", 8)
    # 侃八卦
    gbg = search_news_db([ObjectId("5765050fdcc88e31a7d2e4c3")], 8)
    # 专题
    zt_images = get_head_image("5765057edcc88e31a7d2e4c6", 4)
    zt = search_indexnews_db("579584633c7e431eaf791a06", 3)
    # 热门图集
    rmtj = get_head_image(ObjectId("5768a6f4dcc88e0510fe053a"), 3)
    return render_template('front_list.html', news_list=news_list,
                           detail=detail,
                           hours=hours,
                           zb=zb,
                           yb=yb,
                           gbg=gbg,
                           zt_images=zt_images,
                           lht=lht,
                           zt=zt,
                           rmtj=rmtj,
                           menu=get_menu()
                           )


@index_page.route('/fllist/<channel>/<page>/')
def news_list_page(channel, page=1):
    channel_list_raw = db.Channel.find({"Parent": ObjectId(channel)})
    channel_list = []
    for i in channel_list_raw:
        channel_list.append(i["_id"])
    # condition = {"Channel": {"$in": channel_list}, "Status": 4}
    news_list = db.News.find({"Channel": {"$in": channel_list}}).sort('Published', pymongo.DESCENDING).skip(
        pre_page * (int(page) - 1)).limit(
        pre_page)
    news_dic_list = []
    for i in news_list:
        i["cname"] = db.Channel.find_one({"_id": ObjectId(i["Channel"][0])})["Name"]
        news_dic_list.append(i)
    value = ""
    for i in news_dic_list:
        style = 'style="display: block"'
        if i["Guideimage"] == "":
            style = 'style="display: none"'
        value += "<li %s><p %s><a href='/detail/%s' target='_blank'><img src='%s?w=261&h=171' width='261' height='171'/></a></p><h2><a href='/detail/%s' target='_blank'>%s</a></h2> <h5>%s</h5> <h6>&nbsp;&nbsp;&nbsp;%s<tt><a href='#'>%s</a></tt></h6></li>" % \
                 (style, style, i["_id"], image_server + i["Guideimage"], i["_id"], i["Title"], i["Summary"],
                  datetime_op((i["Published"])), i["cname"])
    return json.dumps(value)


# 领导
@index_page.route('/ld/')
def klj_ld():
    name_list = db.Channel.find({"Parent": ObjectId("57a2ad8edcc88e6ba04499ab")})
    # 王宪魁
    wxkjl = search_news_db([ObjectId("57b26adcdcc88e13050f9156")], 1)
    wxk_three = search_indexnews_db("57b2abe83c7eb9e89a188b7a", 3)
    # 陆昊
    lhjl = search_news_db([ObjectId("57b2832cdcc88e5b4c92ff49")], 1)
    lh_three = search_indexnews_db("57b2abe83c7eb9e89a188b7b", 3)
    # 黄建盛
    hjsjl = search_news_db([ObjectId("57b28344dcc88e5b4166a927")], 1)
    hjs_three = search_indexnews_db("57b2abe83c7eb9e89a188b7c", 3)
    # 张孝廉
    zxljl = search_news_db([ObjectId("57b2835ddcc88e5b4166a928")], 1)
    zxl_three = search_indexnews_db("57b2abe83c7eb9e89a188b7d", 3)
    # 杨汭
    yrjl = search_news_db([ObjectId("57b28372dcc88e5b4c92ff4a")], 1)
    yr_three = search_indexnews_db("57b2abe83c7eb9e89a188b7e", 3)
    # 陈海波
    chbjl = search_news_db([ObjectId("57b28388dcc88e5b4166a929")], 1)
    chb_three = search_indexnews_db("57b2abe83c7eb9e89a188b7f", 3)
    # 郝会龙
    hhljl = search_news_db([ObjectId("57b28399dcc88e5b4166a92a")], 1)
    hhl_three = search_indexnews_db("57b2abe83c7eb9e89a188b80", 3)
    # 赵敏
    zmjl = search_news_db([ObjectId("57b283a5dcc88e5b4c92ff4c")], 1)
    zm_three = search_indexnews_db("57b2abe83c7eb9e89a188b81", 3)
    # 李海涛
    lhtjl = search_news_db([ObjectId("57b283b3dcc88e5b4166a92b")], 1)
    lht_three = search_indexnews_db("57b2abe83c7eb9e89a188b82", 3)
    # 李雷
    lljl = search_news_db([ObjectId("57b283c1dcc88e5b4166a92c")], 1)
    ll_three = search_indexnews_db("57b2abe83c7eb9e89a188b83", 3)
    return render_template('leaders.html', menu=get_menu(),
                           ld='ld',
                           name_list=name_list,
                           wxkjl=wxkjl,
                           wxk_three=wxk_three,
                           lhjl=lhjl,
                           lh_three=lh_three,
                           hjsjl=hjsjl,
                           hjs_three=hjs_three,
                           zxljl=zxljl,
                           zxl_three=zxl_three,
                           yrjl=yrjl,
                           yr_three=yr_three,
                           chbjl=chbjl,
                           chb_three=chb_three,
                           hhljl=hhljl,
                           hhl_three=hhl_three,
                           zmjl=zmjl,
                           zm_three=zm_three,
                           lhtjl=lhtjl,
                           lht_three=lht_three,
                           lljl=lljl,
                           ll_three=ll_three
                           )


@index_page.route('/ld/<id>/')
def klj_ld_list(id):
    lingdao = db.Channel.find_one({"numid": int(id)})
    parent = lingdao["_id"]
    order = lingdao["OrderNumber"]
    channel = db.Channel.find({"Parent": ObjectId(parent)}).sort("OrderNumber")
    jianghua = search_news_db([channel[0]["_id"]], 6)
    huodong = search_news_db([channel[1]["_id"]], 6)
    jianli = search_news_db([channel[2]["_id"]], 1)
    index_channel = db.IndexChannel.find_one(
        {"Parent": "57a2ad8edcc88e6ba04499ab", "Type": 2, "order": order})["_id"]
    image_four = search_indexnews_db(index_channel, 4)
    return render_template('leaders_2nd.html', jianghua=jianghua,
                           jianli=jianli,
                           huodong=huodong,
                           image_four=image_four,
                           lingdao=lingdao,
                           ld2nd='ld2nd'
                           )


@index_page.route('/ld/<id>/<num>/<page>')
def klj_ld_list_detail(id, num, page):
    lingdao = db.Channel.find_one({"numid": int(id)})
    parent = lingdao["_id"]
    channel = db.Channel.find({"Parent": ObjectId(parent)}).sort("OrderNumber")
    news_list = []
    name = ''
    if num == "1":
        news_list = search_news_db([channel[0]["_id"]], 12)
        name = "讲话"
    elif num == "2":
        news_list = search_news_db([channel[1]["_id"]], 12)
        name = "活动"
    return render_template("leaders_3rd.html", news_list=news_list, name=name, lingdao=lingdao, ld2nd='ld2nd')


def get_name(channel):
    name = db.Channel.find_one({"_id": ObjectId(channel)})["Name"]
    return name
