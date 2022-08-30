from flask import Flask, jsonify, request
# from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from functools import wraps
from db import db, users_collection
from user.model import User


app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})
bcrypt = Bcrypt(app)
secret = "***************"


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
    res_data = {}
    message = ""
    code = 500
    status = "fail"
    try:
        data = request.get_json()
        check = db['myDB'].find({"email": data['email']})
        email_found = db['users'].find_one({"email": data['email']})
        if email_found:
            message = 'This Email is already registered'
            status = "fail"
            return jsonify({'status': status, "message": message}), 200
        else:
            data['password'] = bcrypt.generate_password_hash(
            data['password']).decode('utf-8')
            data['created'] = datetime.now()
            res  = db["users"].insert_one(data)
            if res.acknowledged:
                status = "successful"
                message = "user created successfully"
                code = 201
    except Exception as ex:
        message = f"{ex}"
        status = "fail"
        code = 500
    return jsonify({"Email": data["email"],"First Name": data["fname"],"Last Name": data["lname"], "message": message}), 200

@app.route('/login', methods=['POST' , 'GET'])
def login():
    message = ""
    res_data = {}
    code = 500
    status = "fail"
    try:
        data = request.get_json()
        user = db["users"].find_one({"email": f'{data["email"]}'})

        if user:
            user['_id'] = str(user['_id'])
            if user and bcrypt.check_password_hash(user['password'], data['password']):
                time = datetime.utcnow() + timedelta(hours=24)
                token = jwt.encode({
                        "user": {
                            "phone": f"{user['phone']}",
                            "email": f"{user['email']}",
                            "id": f"{user['_id']}",
                        },
                        "exp": time
                    },secret)

                del user['password']

                message = f"user authenticated"
                code = 200
                status = "successful"
                res_data['token'] = token.encode().decode('utf-8')
                res_data['user'] = user

            else:
                message = "wrong password"
                code = 401
                status = "fail"
        else:
            message = "invalid login details"
            code = 401
            status = "fail"

    except Exception as ex:
        message = f"{ex}"
        code = 500
        status = "fail"
    return jsonify({'status': status, "data": res_data, "message":message}), code


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8000')
