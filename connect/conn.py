# -*- coding: utf-8 -*-
import redis
from flask_pymongo import MongoClient

__author__ = 'wanglina'


# mongodb master method (can write and read)
def mongo_conn():
    client = MongoClient(
        # 正式服务器
        # "mongodb://china_hlj235811:N3E]RW,dbWfrr0MgKw]Z@125.211.222.234:38898,221.208.194.152:38898/chinahlj?authMechanism=SCRAM-SHA-1"
        # 测试服务器
        # "mongodb://chinahlj_user:chinahlj_user123@192.168.22.101:27638/chinahlj?authMechanism=SCRAM-SHA-1"
        # 本地测试
        "mongodb://chinahlj_user:chinahlj_user123@125.211.222.237:27638/chinahlj?authMechanism=SCRAM-SHA-1"
    )
    db = client["chinahlj"]
    return db


def mongo_conn_master():
    client = MongoClient(
        # 本地测试
        "mongodb://chinahlj_user:chinahlj_user123@125.211.222.237:27638/chinahlj?authMechanism=SCRAM-SHA-1"
        # 测试服务器
        # "mongodb://chinahlj_user:chinahlj_user123@192.168.22.101:27638/chinahlj?authMechanism=SCRAM-SHA-1"
        # 正式服务器
        # "mongodb://china_hlj235811:N3E]RW,dbWfrr0MgKw]Z@125.211.222.238:38898/chinahlj?authMechanism=SCRAM-SHA-1"
    )
    db = client["chinahlj"]
    return db
