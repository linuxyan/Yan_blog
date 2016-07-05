from flask import Flask
from flask import render_template
import os,markdown
from python_redis import python_redis

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

@app.template_filter('custom_markdown')
def custom_markdown(value):
    return markdown.markdown(value.decode('utf-8'),
                            extensions = ['markdown.extensions.fenced_code','markdown.extensions.codehilite'],
                            safe_mode=True,
                            enable_attributes=False)

basedir = os.path.abspath(os.path.dirname(__file__))
app_redis = python_redis.AppRedis()

@app.route('/', methods=['GET'])
def index():
    datalist = app_redis.getalldata()
    return render_template('index.html',datalist=datalist)

@app.route('/content/<int:id>.html', methods=['GET'])
def content(id):
    redis_data = app_redis.hmget(id,'title','md_path')
    title = redis_data[0]
    md_path = redis_data[1]
    data = open(basedir+'/'+md_path).read()
    return render_template('content.html',title=title,data=data)

if __name__ == '__main__':
    app.run()
