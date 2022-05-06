from datetime import datetime

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.second


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detail/<idx>')
def detail(idx):
    post = db.second.find_one({'idx': int(idx)}, {'_id': False})
    return render_template("detail.html", post=post)

@app.route('/articleList', methods=['GET'])
def get_article_list():
    article_list = list(db.second.find({}, {'_id': False}).sort([("reg_date", -1)]))

    for article in article_list:
        article['reg_date'] = article['reg_date'].strftime('%Y.%m.%d %H:%M:%S')

    return jsonify({"article_list": article_list})

# Create
@app.route('/article', methods=['POST'])
def create_article():
    title = request.form.get('title')
    content = request.form.get('content')
    pw = request.form.get('pw')
    read_count = request.form.get('read_count')
    post_count = db.test.estimated_document_count({})

    if post_count == 0:
        max_value = 1
    else:
        # max_value = db.test.find_one(sort=[("idx", -1)])['idx'] + 1 이 부분에 질문이 있어서 아래처럼 구현해도 가능합니다.
        max_value = (list(db.second.find({}).sort([("idx", -1)])))[0]['idx'] + 1

    post = {
        'idx': max_value,
        'title': title,
        'content': content,
        'pw': pw,
        'read_count' : read_count,
        'reg_date': datetime.now()
    }
    db.second.insert_one(post)
    return {"result": "success"}

# Read
# @app.route('/article', methods=['GET'])
# def read_article():
#     article = 0
#     return jsonify({"article": article})
#
# Update
@app.route('/article', methods=['PUT'])
def update_article():
    title = request.args.get('title')
    content = request.args.get('content')
    db.second.update.one({'title' : title}, {'content' : content})
    return {"result": "success"}

# Delete
@app.route('/article', methods=['DELETE'])
def delete_article():
    idx = request.args.get('idx')
    db.second.delete_one({'idx': int(idx)})
    return {"result": "success"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)