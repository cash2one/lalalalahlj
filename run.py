from flask import Flask, render_template
from longwang.index_views import index_page
import sys
reload(sys)
sys.setdefaultencoding("utf8")

app = Flask(__name__)
app.register_blueprint(index_page)


if __name__ == '__main__':
    app.run(debug=True)
