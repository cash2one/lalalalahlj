# coding: utf-8
from flask import Flask
from longwang.index_views import index_page
from longwang.kbg_views import kbg_page
from longwang.psd_views import psd_page
from longwang.mongodb_news import image_server
from longwang.klj_views import klj_page
import sys
reload(sys)
sys.setdefaultencoding("utf8")

app = Flask(__name__)
app.register_blueprint(index_page)
app.register_blueprint(kbg_page)
app.register_blueprint(psd_page)
app.register_blueprint(klj_page)


# Context处理器 相当于页面渲染之前一个拦截器:当前是处理页面图片跳转链接加域名
@app.context_processor
def utility_processor():
    def format_http_url(string="Undefined"):
        if string == "Undefined":
            return ""
        return u'{0}'.format(image_server + string)

    return dict(format_http_url=format_http_url)


if __name__ == '__main__':
    app.run(debug=False)
