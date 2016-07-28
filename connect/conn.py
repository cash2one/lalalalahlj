# -*- coding: utf-8 -*-
import redis
from flask_pymongo import MongoClient

__author__ = 'wanglina'


# mongodb master method (can write and read)
def mongo_conn():
    client = MongoClient(
        # 本地测试
        "mongodb://chinahlj_user:chinahlj_user123@125.211.222.237:27638/chinahlj?authMechanism=SCRAM-SHA-1"
        # 测试服务器
        # "mongodb://chinahlj_user:chinahlj_user123@192.168.22.101:27638/chinahlj?authMechanism=SCRAM-SHA-1"
    )
    db = client["chinahlj"]
    return db


# redis connection method
def redis_conn():
    # 本地测试
    pool = redis.ConnectionPool(host="125.211.222.237", port="24378", password="r233xdggt32_53dv8r39cgsadh5ef23412yhvsd2314gzsdd12")
    # 测试服务器
    # pool = redis.ConnectionPool(host="192.168.22.100", port="24378", password="r233xdggt32_53dv8r39cgsadh5ef23412yhvsd2314gzsdd12")
    r = redis.Redis(connection_pool=pool)
    pipe = r.pipeline()
    pipe.execute()
    return r
