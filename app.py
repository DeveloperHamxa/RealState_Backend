from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS 
from bson import ObjectId
import pymongo
from pymongo import MongoClient
import json
import jwt
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from functools import wraps


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
bcrypt = Bcrypt(app)
secret = "***************"

client = pymongo.MongoClient('mongodb+srv://Hamxa:Hamxa.123@mydb.p3gucfo.mongodb.net/?retryWrites=true&w=majority')
db = client["myDB"]
users_collection = db["RealEstate"]
print(client.list_database_names())


def tokenReq(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            try:
                jwt.decode(token, secret)
            except:
                return jsonify({"status": "fail", "message": "unauthorized"}), 401
            return f(*args, **kwargs)
        else:
            return jsonify({"status": "fail", "message": "unauthorized"}), 401
    return decorated

@app.route('/')
def func():
    return "Real Estate API", 200

@app.route('/signup', methods=['POST', "GET"])
def save_user():
    message = ""
    code = 500
    status = "fail"
    try:
        data = request.get_json()
        check = db['myDB'].find({"email": data['email']})
        data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        data['created'] = datetime.now()
        res = users_collection.insert_one(data) 
        if res.acknowledged:
                status = "successful"
                message = "user created successfully"
                code = 201
    except Exception as ex:
        message = f"{ex}"
        status = "fail"
        code = 500
    return jsonify({'status': status, "message": message}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8000')