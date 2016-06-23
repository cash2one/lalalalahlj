# -*- coding: utf-8 -*-
import redis
from flask.ext.pymongo import MongoClient

__author__ = 'wanglina'


# mongodb master method (can write and read)
def mongo_conn():
    client = MongoClient(
        "mongodb://chinahlj_user:chinahlj_user123@125.211.222.237:27638/chinahlj?authMechanism=SCRAM-SHA-1")
    db = client["chinahlj"]
    return db


# redis connection method
def redis_conn():
    pool = redis.ConnectionPool(host="118.144.86.65", port="13378", password="idx89jmp_73ub4r39xolhjsu633cm2pvms67")
    r = redis.Redis(connection_pool=pool)
    pipe = r.pipeline()
    pipe.execute()
    return r
