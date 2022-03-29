from crypt import methods
from pydoc import cli
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import jwt # pip install PyJWT
import datetime
import hashlib # sha256을 사용하기 위한 모듈
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = b'xr43321\n\xec'

client = MongoClient('localhost', 27017)
db = client.dbHotMusic

# JWT 토큰을 만들기 위한 비밀키값입니다.
# 아무거나 넣어도 상관없음
# 서버만 알고 있기 때문에, 내 서버 안에서 인코딩(암호화), 디코딩(복호화)를 할 수 있습니다.
SECRET_KEY = 'JungleHotMusic'

admin_id = 'admin'
admin_pw = '1234'


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

    register_check = db.user.find_one({'id':id_receive})

    if register_check != None:
        return jsonify({'result':'fail'})
    else:
        pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
        db.user.insert_one({'id':id_receive, 'pw':pw_hash})

    return jsonify({'result' : 'success'})


@app.route('/login_confirm', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    print(pw_hash)

    login_check = db.user.find_one({'id':id_receive, 'pw':pw_hash})

    if login_check != None:
        payload = {
            'id' : id_receive,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        print(token)

        return jsonify({'result':'success', 'token':token})
    else:
        return jsonify({'result':'fail', 'msg':'아이디/비밀번호가 일치하지 않습니다.'})




if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)