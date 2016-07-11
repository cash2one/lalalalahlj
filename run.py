from flask import Flask
from longwang.index_views import index_page
from longwang.kbg_views import kbg_page
from longwang.psd_views import psd_page
import sys
reload(sys)
sys.setdefaultencoding("utf8")

app = Flask(__name__)
app.register_blueprint(index_page)
app.register_blueprint(kbg_page)
app.register_blueprint(psd_page)


if __name__ == '__main__':
    app.run(debug=True)
