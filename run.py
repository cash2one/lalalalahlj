# coding: utf-8
from flask import Flask
from longwang.index_views import index_page
from longwang.kbg_views import kbg_page
from longwang.psd_views import psd_page
from longwang.klj_views import klj_page
from longwang.zt_views import zt_page
from longwang.sjlj_views import sjlj_page
from longwang.wap_site.index_views import wap_page


import sys

reload(sys)
sys.setdefaultencoding("utf8")

app = Flask(__name__)
app.register_blueprint(index_page)  # web_首页
app.register_blueprint(kbg_page)  # web_侃八卦
app.register_blueprint(psd_page)  # web_品深度
app.register_blueprint(klj_page)  # web_看龙江
app.register_blueprint(zt_page)  # web_专题
app.register_blueprint(sjlj_page)  # web_数据龙江
app.register_blueprint(wap_page)  # wap_网站

# 专题的上传路径
app.config['UPLOAD_FOLDER'] = '/zt/'

if __name__ == '__main__':
    app.run(debug=True)
