from pydoc import cli
from typing import List
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import jwt # pip install PyJWT
import datetime
import hashlib # sha256을 사용하기 위한 모듈
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbHotMusic

# JWT 토큰을 만들기 위한 비밀키값입니다.
# 아무거나 넣어도 상관없음
# 서버만 알고 있기 때문에, 내 서버 안에서 인코딩(암호화), 디코딩(복호화)를 할 수 있습니다.
app.secret_key = b'xr43321\n\xec'

admin_id = 'admin'
admin_pw = '1234'

# 임시 추가
@app.route('/')
def main():
    # 더미 정보
    # 회원의 플레이리스트
    myList_get = [{'title': 'title_1', 'artist': 'artist_1', 'clickurl': 'clickURL_1'}, {'title': 'title_2', 'artist': 'artist_2', 'clickurl': 'clickURL_2'}]
    # 랭킹 100 정보
    charts = list(db.charts.find({}, {'_id': False}))
   
    
    # 화면 랜더링
    return render_template('main.html', is_login = "True", myList= myList_get , musics = charts)

@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'id':id_receive, 'pw':pw_hash})

    return jsonify({'result' : 'success'})


@app.route('/login_confirm', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    print(id_receive, pw_receive)
    return jsonify({'result' : 'success'})


@app.route('/playlist', methods=['POST'])
def insert_playlist():
    artist_receive = request.form['artist_give']
    title_receive = request.form['title_give']
    
    
    list = {"artist" : artist_receive, "title" : title_receive}

    db.playlist.insert_one(list)
    
    return jsonify({'result':'success', 'msg': '플레이리스트 추가 완료!'})
    



if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)