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

class Base(Resource):
    def __init__(self):
        self.table = ''

    @auth.login_required
    def get(self, key=None):
        if key != None:
            r = db.fetch(self.table, key)
            print(r)
            if len(r) != 0:
                result = r[0][1]
            else:
                result = ""
            return make_response(result)
        else:
            r = db.fetchall(self.table)
            result = []
            for i in r:
                result.append(i[1])
            return result
    
    @auth.login_required
    def post(self, key):
        data = request.get_json()
        val = data['val']
        db.insert(self.table, key, val)
        return 'succeed'
    
    @auth.login_required
    def delete(self, key=None):
        if key != None:
            db.delete(self.table, key)
        else:
            db.clear(self.table)
        return {'status': 'succeed'}

class Entries(Base):
    def __init__(self):
        self.table = 'entries'

class Highlights(Base):
    def __init__(self):
      self.table = 'highlights' 

class Questions(Base):
    def __init__(self):
        self.table = 'questions'

    @auth.login_required
    def get(self, key=None):
        if key != None:
            r = db.fetch(self.table, key)
            result = json.loads(r[0][1])
        else:
            r = db.fetchall(self.table)
            result = []
            for one in r:
                result.append(json.loads(one[1]))
        return result

class Settings(Base):
    def __init__(self):
        self.table = 'settings'

class TrackingEntries(Base):
    def __init__(self):
        self.table = 'trackingEntries'

class TrackingQuestions(Base):
    def __init__(self):
        self.table = 'trackingQuestions'

class Keys(Resource):
    @auth.login_required
    def get(self, table):
        r = db.fetchkeys(table)
        result = []
        for x in r:
            result.append(x[0])
        return result
    
api.add_resource(Keys, '/journal/keys/<table>')
api.add_resource(Entries, '/journal/entries/<key>', '/journal/entries')
api.add_resource(Highlights, '/journal/highlights/<key>', '/journal/highlights')
api.add_resource(Questions, '/journal/questions/<key>', '/journal/questions')
api.add_resource(Settings, '/journal/settings/<key>', '/journal/settings')
api.add_resource(TrackingEntries, '/journal/trackingEntries/<key>', '/journal/trackingEntries')
api.add_resource(TrackingQuestions, '/journal/trackingQuestions/<key>', '/journal/trackingQuestions')

def inittable():
    db.create_table('entries')
    db.create_table('highlights')
    db.create_table('questions')
    db.create_table('settings')
    db.create_table('trackingEntries')
    db.create_table('trackingQuestions')

inittable()

if __name__ == "__main__":
    app.run(host='0.0.0.0')