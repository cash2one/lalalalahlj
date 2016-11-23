# coding=utf-8
import json
import os
import urllib

from bs4 import BeautifulSoup
from bson import ObjectId
from flask import Blueprint, render_template, request, current_app, Response, make_response
from connect import conn
import sys

reload(sys)
sys.setdefaultencoding('utf8')
# import pymongo

zt_page = Blueprint('zt_page', __name__, template_folder='templates')
db = conn.mongo_conn_master()


# 添加专题文件
@zt_page.route('/zt/add/<id>/', methods=['POST', 'GET'])
def zt_add(id):
    if request.method == "POST":
        pro = db["File_upload"]
        f = request.files['topImage3']
        r_path = ""
        name = ""
        uploadurl = ""
        nid = ""
        _title, _ext = os.path.splitext(f.filename)
        if f != "" and f != None:
            # try:
            fext = str(_ext).lower().replace(".", "")
            if fext == 'jpg' or fext == "png" or fext == "jpeg" or fext == "bmp":
                mkdir_path(id + "/img/")
                uploadurl = upload_path(id + "/img/" + _title + _ext)
                f.save(uploadurl)
                r_path = relative_path(id + "/img/" + _title + _ext)
            else:
                if fext == "css":
                    mkdir_path(id + "/css/")
                    uploadurl = upload_path(id + "/css/" + _title + _ext)
                    f.save(uploadurl)
                    r_path = relative_path(id + "/css/" + _title + _ext)
                if fext == "js":
                    mkdir_path(id + "/js/")
                    uploadurl = upload_path(id + "/js/" + _title + _ext)
                    f.save(uploadurl)
                    r_path = relative_path(id + "/js/" + _title + _ext)
                if fext == "html":
                    mkdir_path(id)
                    uploadurl = upload_path(id + "/" + _title + _ext)
                    f.save(uploadurl)
                    html = f.read()
                    soup = BeautifulSoup(html)
                    if str(soup.original_encoding) != 'utf-8':
                        for i in html:
                            # print str(i).decode('gb2312').encode('utf-8')
                            open(uploadurl).write(str(i).decode('gb2312').encode('utf-8'))

                    r_path = relative_path(id + "/" + _title + _ext)
            if fext not in ["jpg", "png", "jpeg", "bmp", "js", "css", "html"]:
                mkdir_path(id + "/others/")
                uploadurl = upload_path(id + "/others/" + _title + _ext)
                f.save(uploadurl)
                r_path = relative_path(id + "/others/" + _title + _ext)

            r_path = r_path.replace("zt", "zuanti")
            insertinfo = {
                "name": _title + _ext,
                "url": r_path,
                "newsid": id,
                "type": _ext,
                "index": 0,
                "status": 0
            }
            file = pro.find({"newsid": id, "url": r_path})
            # 判断数据库中是否存在  不存在时插入
            if file.count() == 0:
                pro.insert(insertinfo)
            else:  # 覆盖的状态改为1
                pro.update(
                    {"_id": ObjectId(pro.find_one({"newsid": id, "url": r_path})["_id"])},
                    {"$set": {"status": 1}})
            # 返回更新后的编号
            nid = str(pro.find_one({"newsid": id, "url": r_path})["_id"])
            # except Exception, e:
            #     return json.dumps({"status": e.message})
            result = '{"url":"' + r_path + '","status":"' + str(
                200) + '","name":"' + name + _ext + '","type":"' + _ext + '","id":"' + nid + '"}'
            res = "jsonpCallback1(" + result + ")"
            return res_result(res)
    else:
        result = '{"status":"' + str(400) + '"}'
        res = "jsonpCallback1(" + result + ")"
        return res_result(res)


# 修改专题文件
@zt_page.route('/zt/modify/', methods=['POST', 'GET'])
def zt_modify():
    if request.method == "POST":
        _id = request.values.get("id")
        content = request.values.get("content")
        pro = db["File_upload"]
        files = pro.find_one({"_id": ObjectId(_id)})
        file_handle = open(os.path.normpath(os.path.join(os.path.dirname(__file__), "../")) + (
            str(files["url"]).replace("zuanti", "zt")), "w")
        file_handle.write(str(content).encode("utf-8"))
        result = '{"status":"' + str(200) + '"}'
        res = "jsonpCallback1(" + result + ")"
        return res_result(res)
    else:
        result = '{"status":"' + str(400) + '"}'
        res = "jsonpCallback1(" + result + ")"
        return res_result(res)


# 删除
@zt_page.route('/zt/delete/<id>/', methods=['POST', 'GET'])
def zt_delete(id):
    if request.method == "GET":
        pro = db["File_upload"]
        files = pro.find_one({"_id": ObjectId(id)})
        rmdir_path(str(files["url"]).replace("zuanti", "zt"))
        pro.remove({"_id": ObjectId(id)})
        result = '{"status":"' + str(200) + '","id":"' + id + '"}'
        res = "jsonpCallback1(" + result + ")"
        return res_result(res)
    else:
        result = '{"status":"' + str(400) + '"}'
        res = "jsonpCallback1(" + result + ")"
        return res_result(res)


# 获取文件内容
@zt_page.route('/zt/get/<id>/', methods=['POST', 'GET'])
def zt_get(id):
    if request.method == "GET":
        pro = db["File_upload"]
        url = os.path.normpath(os.path.join(os.path.dirname(__file__), "../")) + pro.find_one({"_id": ObjectId(id)})[
            "url"]
        result = '{"status":"' + str(200) + '","file":"' + str(open(url.replace("zuanti", "zt")).read()).replace("\r",
                                                                                                                 "").replace(
            "\n",
            "").replace(
            "\n\r", "").replace("\r\n", "") + '"}'
        res = "jsonpCallback1(" + result + ")"
        return res_result(res)
    else:
        result = '{"status":"' + str(400) + '"}'
        res = "jsonpCallback1(" + result + ")"
        return res_result(res)


# 设置专题首页
@zt_page.route('/zt/index/<id>/', methods=['POST', 'GET'])
def zt_index(id):
    if request.method == "GET":
        pro = db["File_upload"]
        index = pro.find_one({"_id": ObjectId(id)})["index"]
        if index == 1:
            pro.update({"_id": ObjectId(id)}, {"$set": {"index": 0}})
        else:
            pro.update({"_id": ObjectId(id)}, {"$set": {"index": 1}})
        result = '{"status":"' + str(200) + '"}'
        res = "jsonpCallback1(" + result + ")"
        return res_result(res)
    else:
        result = '{"status":"' + str(400) + '"}'
        res = "jsonpCallback1(" + result + ")"
        return res_result(res)


# 文件上传的全路径
def upload_path(file_name):
    return os.path.join(
        os.path.normpath(os.path.join(os.path.dirname(__file__), "../")) + current_app.config["UPLOAD_FOLDER"],
        file_name)


# 文件上传的相对路径
def relative_path(file_name):
    return os.path.join(current_app.config["UPLOAD_FOLDER"], file_name)


# 创建文件夹
def mkdir_path(file_path):
    path = os.path.join(
        os.path.normpath(os.path.join(os.path.dirname(__file__), "../")) + current_app.config["UPLOAD_FOLDER"],
        file_path)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception, e:
            print e.message


# 删除文件
def rmdir_path(file_path):
    path = os.path.join(
        os.path.normpath(os.path.join(os.path.dirname(__file__), "../")) + current_app.config["UPLOAD_FOLDER"],
        file_path)
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception, e:
            print e.message


# response 返回
def res_result(result):
    res = make_response(result)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


# 设置专题首页
# @zt_page.route('/zt/test/', methods=['POST', 'GET'])
def test():
    uploadurl = "C:\Users\wanglina\Desktop/gb2312.html"
    soup = BeautifulSoup(open(uploadurl).read())
    if str(soup.original_encoding) != 'utf-8':
        # f = open(uploadurl, "r")
        # g_u = f.read().decode('gb2312').encode('utf-8')
        rl = open(uploadurl)
        for i in rl:
            # print str(i).decode('gb2312').encode('utf-8')
            g_u = str(i).decode('gb2312').encode('utf-8')
            # print g_u
    return "nice"
