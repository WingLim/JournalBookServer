from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_httpauth import HTTPTokenAuth
from db_sqlite import DBSqlite
from utils import db2dict
from config import pwd
import json
import config

app = Flask(__name__)
CORS(app)
api = Api(app)
db = DBSqlite()
auth = HTTPTokenAuth(scheme="Token")

@auth.verify_token
def verify_token(token):
    if token == pwd:
        return True
    return False

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

class Journal(Resource):
    @auth.login_required
    def get(self):
        table = request.args.get('table')
        key = request.args.get('key')
        jtype = request.args.get('type')
        # 获取全部
        if jtype == 'all':
            pass
        # 获取特定对象
        elif jtype == 'object':
            pass
        # 获取所有 key
        elif jtype == 'keys':
            r = db.fetchkeys(table)
            result = []
            for x in r:
                result.append(x[0])
        # 普通获取
        else:
            r = db.fetch(table, key)
            if len(r) != 0:
                try:
                    result = json.loads(r[0][1])
                except json.decoder.JSONDecodeError:
                    result = r[0][1]
            else:
                result = []
        return result

    @auth.login_required
    def post(self):
        data = request.get_json()
        table = data['table']
        key = data['key']
        val = data['val']
        db.insert(table, key, val)
        return 'succeed'

    @auth.login_required
    def delete(self):
        table = request.form['table']
        key = request.form['key']
        jtype = request.form['type']
        # 清空整个表
        if jtype == 'clear':
            pass

api.add_resource(Journal, '/journal')

if __name__ == "__main__":
    app.run()