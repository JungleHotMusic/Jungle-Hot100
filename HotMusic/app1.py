from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbjungle


@app.route('/')
def home():
    return render_template('main.html')

@app.route('/list', methods=['GET'])
def show_charts():
   
    charts = list(db.charts.find({}, {'_id': False}))
    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success', 'charts_list': charts})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)