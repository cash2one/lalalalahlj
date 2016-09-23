# -*- coding: utf-8 -*-#
# filename:mongodb_news.py
# __author__ = 'wanglina'
import datetime
import time
from bson import ObjectId
import pymongo
from connect import conn

db = conn.mongo_conn()

# image_server = "http://125.211.222.237:17937/"
image_server = "http://www.hljpic.cn/"
ym_server = "http://www.chinahlj.cn"


# 根据编号  是否带图  调取的条数 新闻编号列表  新闻类型 是否推荐
def search_news_db(Channel, limit, Guideimage=0, list_db=[]):
    condition = {"Channel": {"$in": Channel}, "Status": 4}
    if Guideimage == 1:
        condition.update({"Guideimage": {"$ne": ""}})
    if list_db != []:
        id_list = []
        for news_detail in list_db:
            id_list.append(int(news_detail["_id"]))
        condition.update({"numid": {"$nin": id_list}})
    news_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).limit(limit)
    news_db_list = []
    try:
        for news_detail in news_list:
            news_db_list.append(get_mongodb_dict(news_detail))
    except:
        # 当有乱码问题导致报错时，直接跳过重新获取新的新闻条目
        news_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).skip(limit).limit(limit)
        for news_detail in news_list:
            news_db_list.append(get_mongodb_dict(news_detail))
        pass
    return news_db_list


# 获取新闻二级频道列表
def get_child_column_list(column_id):
    two_column_list = db.news_column.find({"parent_id": int(column_id), "is_head": 0}).sort('sort')
    return two_column_list


# 获取新闻二级频道列表
def get_hot_list(column_id):
    hot_list = []
    try:
        hot_list = db.news_hot_words.find({"column_id": int(column_id)}).sort('hot_time', pymongo.DESCENDING)[0]
    except Exception, e:
        pass
    return hot_list


# 根据mongodb按照条件取出的数据重新
def get_mongodb_dict(i):
    new_dict = {}
    new_dict["_id"] = i["numid"]
    new_dict["title"] = i["Title"]
    new_dict["summary"] = i["Summary"]
    new_dict["images"] = i["Images"]
    new_dict["guide_image"] = i["Guideimage"] if i["Guideimage"] == "" else image_server + i["Guideimage"]
    new_dict["publish_time"] = datetime_op(i["Published"])
    new_dict["cid"] = i["channelnumid"][0]
    try:
        new_dict["cname"] = db.Channel.find_one({"_id": ObjectId(i["Channel"][0])})["Name"]
        new_dict["href"] = db.Channel.find_one({"_id": ObjectId(i["Channel"][0])})["Href"]
    except:
        pass
    # new_dict["href"] = db.news_column.find_one({"_id": int(i["column_id"]["id"])})["des"]
    return new_dict


# 把string类型的时间转换成datetime类型
def switch_string_to_time(string):
    publish_time = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
    if publish_time.year < 1900:  # 有些时间抓取错误所以做特殊处理
        publish_time = datetime.datetime.now()
    return publish_time


# 把datetime转成字符串
def dt_to_s(dt):
    return dt.strftime("%Y-%m-%d-%H")


# 把字符串转成时间戳形式
def s_to_t(strTime):
    return time.mktime(switch_string_to_time(strTime).timetuple())


# 把时间戳转成字符串形式
def t_to_s(stamp):
    return time.strftime("%Y-%m-%d-%H", time.localtime(stamp))


# 把datetime类型转外时间戳形式
def d_to_s(dateTime):
    return time.mktime(dateTime.timetuple())


# 轮换图
def get_head_image(channel, limit):
    lht = db.ChannelHeadImage.find({"ChannelID": ObjectId(channel)}).sort("no").limit(limit)
    _lht = []
    for i in lht:
        dd = db.News.find_one({"_id": ObjectId(i["NewsID"])})
        new_dict = {}
        new_dict["_id"] = i["numid"]
        new_dict["title"] = i["Title"]
        new_dict["guide_image"] = image_server + i["HeadImage"]
        new_dict["summary"] = dd["Summary"]
        new_dict["publish_time"] = datetime_op(dd["Published"])
        _lht.append(new_dict)
    return _lht


def get_images(_list):
    list = db.News.find({"_id": {"$in": _list}, "Status": 4}).sort('Published', pymongo.DESCENDING)
    _list = []
    for i in list:
        _list.append(get_mongodb_dict(i))
    return _list


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


# 获取组版新闻
def search_indexnews_db(Channel, limit):
    condition = {"ChannelId": str(Channel)}
    news_list = db.IndexNews.find(condition).sort("orderno").limit(limit)
    _news_list = []
    for i in news_list:
      try:
        new_dict = {}
        new_dict["_id"] = i["numid"]
        new_dict["title"] = i["Title"]
        new_dict["guide_image"] = image_server + i["image"]
        new_dict["summary"] = db.News.find_one({"_id": ObjectId(i["NewsID"])})["Summary"]
        _news_list.append(new_dict)
      except:
          pass
    return _news_list


# 头条新闻
def get_image_news(channel, limit, list_db=[]):
    condition = {"ChannelId": channel}
    if list_db != []:
        id_list = []
        for news_list in list_db:
            id_list.append(news_list["_id"])
        condition.update({"numid": {"$nin": id_list}})
    lht = db.IndexNews.find(condition).sort("no").limit(limit)
    _lht = []
    for i in lht:
        new_dict = {}
        new_dict["_id"] = i["numid"]
        new_dict["title"] = i["Title"]
        new_dict["guide_image"] = image_server + i["image"]
        new_dict["summary"] = db.News.find_one({"_id": ObjectId(i["NewsID"])})["Summary"]
        _lht.append(new_dict)
    return _lht
