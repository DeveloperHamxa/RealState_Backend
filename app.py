from flask import Flask, jsonify, request
import jwt
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from functools import wraps
from db import db
from bson import json_util
import json


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

@app.route('/profile')
def my_profile():
    response_body = {
        "name": "Nagato",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body


@app.route('/signup', methods=['POST'])
def save_user():
    message = ""
    code = 500
    status = "fail"
    try:
        data = request.get_json()
        email_found = db['users'].find_one({"email": data['email']})
        if email_found:
            message = 'This Email is already registered'
            status = "fail"
            return jsonify({'status': status, "message": message}), 200
        else:
            # hashing the password so it's not stored in the db as it was 
            data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            data['created'] = datetime.now()

            #this is bad practice since the data is not being checked before insert
            res = db["users"].insert_one(data) 
            if res.acknowledged:
                status = "successful"
                message = "user created successfully"
                code = 201
    except Exception as ex:
        message = f"{ex}"
        status = "fail"
        code = 500
    return jsonify({'status': status, "message": message}), 200

@app.route('/login', methods=['POST', 'GET'])
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
                }, secret)

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
    return jsonify({'status': status, "data": res_data, "message": message}), code


@app.route('/addproperty', methods=['POST', "GET"])
def add_property():
    data = request.get_json()
    Property_Name=data['Property Name']
    Location=data['Location']
    Property_Type=data['Property Type']
    Area=data['Area']
    Finish_Type=data['Finish Type']
    res = db["estate"].insert_one({"Property": Property_Name, "Property Type": Property_Type, "Location": Location, "Area": Area, "Finish Type": Finish_Type})
    # res = db["estate"].insert_one(data)
    if res.acknowledged:
        status = "successful"
        message = "state created successfully"
        code = 201
        return jsonify({'status': status, "message": message}), code

    else:
        status = "successful"
        message = "Estate is not Created"
        code = 201
    return jsonify({'status': status, "message": message}), code

@app.route('/property/<name>', methods=['POST', "GET"])
def search_property(name):
    estate_found = db['estate'].find_one({"name": name})
    if estate_found:
        output = {'name': estate_found['name'], 'location': estate_found['location'], 'id': estate_found['_id']}
        page_sanitized = json.loads(json_util.dumps(output))
        return jsonify({'result': page_sanitized})
    else:
        status = "unsuccessful"
        message = "Not Found"
        code = 201
        return jsonify({'status': status, "message": message}), code

@app.route('/allproperty', methods=['GET'])
def index():
    cur = db['estate'].find({}, {'name': 1, 'location': 1 , '_id': 0})
    page_sanitized = json.loads(json_util.dumps(cur))
    return jsonify({'result': page_sanitized})

# @app.route("/add", methods=["POST", "GET"], strict_slashes=False)
# def add_articles():
#     title = request.json['title']
#     body = request.json['body']

#     res= db["estate"].insert_one(title=title,body=body)

    return jsonify(res)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8000')
