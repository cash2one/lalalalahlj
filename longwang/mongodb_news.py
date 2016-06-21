# -*- coding: utf-8 -*-#
# filename:mongodb_news.py
# __author__ = 'wanglina'
import datetime
from bson import ObjectId
import pymongo
from connect import conn

db = conn.mongo_conn()
image_server = "http://125.211.222.237:17937/"


# 根据编号  是否带图  调取的条数 新闻编号列表  新闻类型 是否推荐
def search_news_db(Channel,  limit, list_db=[], newstype=1):
    condition = {"Channel": {"$in": Channel}, "newstype": newstype, "Status": 4}
    # if is_images == 1:
    #     condition.update({"Images": {"$ne": []}})
    if list_db != []:
        id_list = []
        for news_detail in list_db:
            id_list.append(ObjectId(news_detail["_id"]))
        condition.update({"_id": {"$nin": id_list}})
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
    new_dict["_id"] = i["_id"]
    new_dict["title"] = i["Title"]
    new_dict["summary"] = i["Summary"]
    new_dict["images"] = i["Images"]
    new_dict["guide_image"] = image_server + i["Guideimage"]
    new_dict["publish_time"] = i["Published"]
    # new_dict["cid"] = i["column_id"]["id"]
    # new_dict["column"] = i["column_id"]["name"]
    # new_dict["href"] = db.news_column.find_one({"_id": int(i["column_id"]["id"])})["des"]
    return new_dict


# 把string类型的时间转换成datetime类型
def switch_string_to_time(string):
    publish_time = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
    if publish_time.year < 1900:  # 有些时间抓取错误所以做特殊处理
        publish_time = datetime.datetime.now()
    return publish_time


# 根据编号  是否带图  调取的条数 新闻编号列表  是否头题 是否焦点
def search_news_list_db(column_id, is_images, limit, list_db=[], is_head=0, is_focus=0):
    condition = {"column_id.id": {"$in": column_id}, "is_head": is_head, "status": 1}
    if is_images == 1:
        condition.update({"images": {"$ne": []}})
    if list_db != []:
        id_list = []
        for news_detail in list_db:
            id_list.append(ObjectId(news_detail["_id"]))
        condition.update({"_id": {"$nin": id_list}})
    if is_focus == 1:
        condition.update({"is_focus": 1})
    news_list = db.news_detail.find(condition).sort('publish_time', pymongo.DESCENDING).limit(limit)
    news_db_list = []
    try:
        for news_detail in news_list:
            news_db_list.append(get_mongodb_dict(news_detail))
    except:
        # 当有乱码问题导致报错时，直接跳过重新获取新的新闻条目
        news_list = db.news_detail.find(condition).sort('publish_time', pymongo.DESCENDING).skip(limit).limit(limit)
        for news_detail in news_list:
            news_db_list.append(get_mongodb_dict(news_detail))
        pass
    return news_db_list


# 轮换图
def get_head_image(channel, limit):
    lht = db.ChannelHeadImage.find({"ChannelID": ObjectId(channel)}).sort("no", pymongo.DESCENDING).limit(limit)
    _lht=[]
    for i in lht:
        new_dict = {}
        new_dict["_id"] = i["NewsID"]
        new_dict["title"] = i["Title"]
        new_dict["guide_image"] = image_server + i["HeadImage"]
        _lht.append(new_dict)
    return _lht