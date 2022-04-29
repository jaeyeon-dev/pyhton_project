from datetime import datetime

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.test


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detail/<idx>')
def detail(idx):


@app.route('/post', methods=['POST'])
def save_post():
    title_receive = ['title']
    content_receive = ['content']

    today = datetime.now()

    doc = {
        'title': title_receive,
        'content': content_receive,
        'reg_data' : today.strftime('%Y-%m-%d-%H-%M-%S')
    }

    db.memo.insert_one(doc)

    return {"result": "포스팅 성공!"}


@app.route('/post', methods=['GET'])
def get_post():
    posts = 0

    return jsonify({"posts": posts})


@app.route('/post', methods=['DELETE'])
def delete_post():
    idx = request.args.get('idx')
    db.test.delete_one({'idx': int(idx)})
    return {"result": "삭제 성공"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)