# -*- coding: utf-8 -*-
from flask.ext.pymongo import MongoClient


__author__ = 'wanglina'


# mongodb master method (can write and read)
def mongo_conn():
    client = MongoClient("mongodb://chinahlj_user:chinahlj_user123@125.211.222.237:27638/chinahlj?authMechanism=SCRAM-SHA-1")
    db = client["chinahlj"]
    return db
