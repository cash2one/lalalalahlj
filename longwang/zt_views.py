# coding=utf-8
import json
import os

import datetime
from flask import Blueprint, render_template, request, current_app
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
        name = ""
        nid = ""
        _title, _ext = os.path.splitext(f.filename)
        if f != "" and f != None:
            try:
                fext = str(_ext).lower().replace(".", "")
                if fext == 'jpg' or fext == "png" or fext == "jpeg" or fext == "bmp":
                    sltName = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    name = sltName
                    mkdir_path(id + "/img/")
                    uploadurl = upload_path(id + "/img/" + name + _ext)
                    f.save(uploadurl)
                else:
                    if fext == "css":
                        mkdir_path(id + "/css/")
                        uploadurl = upload_path(id + "/css/" + _title + _ext)
                        destination = open(uploadurl, 'wb+')
                        for chunk in f.chunks():
                            destination.write(chunk)
                        name = _title
                    if fext == "js":
                        mkdir_path(id + "/js/")
                        uploadurl = upload_path(id + "/js/" + _title + _ext)
                        destination = open(uploadurl, 'wb+')
                        for chunk in f.chunks():
                            destination.write(chunk)
                        name = _title
                    if fext == "html":
                        mkdir_path(id)
                        uploadurl = upload_path(id+"/" + _title + _ext)
                        destination = open(uploadurl, 'wb+')
                        for chunk in f.chunks():
                            destination.write(chunk)
                        name = _title
                insertinfo = {
                    "name": _title + _ext,
                    "url": uploadurl,
                    "name1": name + _ext,
                    "newsid": id,
                    "type": _ext,
                    "index": 0
                }
                pro.insert(insertinfo)
                nid = str(pro.find_one({"newsid": id, "url": uploadurl})["_id"])
            except Exception, e:
                return json.dumps({"status": e.message})
            return json.dumps({'url': uploadurl, "status": 0, "name": name + _ext, "type": _ext, "id": nid})
    else:
        return json.dumps({"status": 400})


def upload_path(file_name):
    return os.path.join(current_app.config["UPLOAD_FOLDER"], file_name)


def mkdir_path(file_path):
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], file_path)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception, e:
            print e.message
