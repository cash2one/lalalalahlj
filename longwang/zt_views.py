# coding=utf-8
import json
import os

import datetime
from flask import Blueprint, render_template, request, current_app, Response, make_response
from connect import conn

# import pymongo

zt_page = Blueprint('zt_page', __name__, template_folder='templates')
db = conn.mongo_conn()


@zt_page.route('/zt/add/<id>/', methods=['POST', 'GET'])
def zt_add(id):
    if request.method == "POST":
        pro = db["File_upload"]
        f = request.files['topImage3']
        uploadurl = ""
        r_path = ""
        name = ""
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
                    destination = open(uploadurl, 'wb+')
                    for chunk in f.chunks():
                        destination.write(chunk)
                    r_path = relative_path(id + "/css/" + _title + _ext)
                if fext == "js":
                    mkdir_path(id + "/js/")
                    uploadurl = upload_path(id + "/js/" + _title + _ext)
                    destination = open(uploadurl, 'wb+')
                    for chunk in f.chunks():
                        destination.write(chunk)
                    r_path = relative_path(id + "/js/" + _title + _ext)
                if fext == "html":
                    mkdir_path(id)
                    uploadurl = upload_path(id + "/" + _title + _ext)
                    destination = open(uploadurl, 'wb+')
                    for chunk in f.chunks():
                        destination.write(chunk)
                    r_path = relative_path(id + "/" + _title + _ext)
            insertinfo = {
                "name": _title + _ext,
                "url": r_path,
                "newsid": id,
                "type": _ext,
                "index": 0
            }
            count = pro.find({"newsid": id, "url": r_path}).count()
            # 判断数据库中是否存在  不存在时插入
            if count == 0:
                pro.insert(insertinfo)
            # 返回更新后的编号
            nid = str(pro.find_one({"newsid": id, "url": r_path})["_id"])
            # except Exception, e:
            #     return json.dumps({"status": e.message})
            result = '{"url":"' + r_path + '","status":"' + str(
                200) + '","name":"' + name + _ext + '","type":"' + _ext + '","id":"' + nid + '"}'
            # return Response("jsonpCallback" + "(" + result + ")")
            # return Response(result)
            res = make_response(result)
            res.headers['Access-Control-Allow-Origin'] = '*'
            return res
    else:
        return Response(json.dumps({"status": 400}))


# 文件上传的全路径
def upload_path(file_name):
    return os.path.join(os.path.dirname(__file__) + current_app.config["UPLOAD_FOLDER"], file_name)


# 文件上传的相对路径
def relative_path(file_name):
    return os.path.join(current_app.config["UPLOAD_FOLDER"], file_name)


# 创建文件夹
def mkdir_path(file_path):
    path = os.path.join(os.path.dirname(__file__) + current_app.config["UPLOAD_FOLDER"], file_path)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception, e:
            print e.message
