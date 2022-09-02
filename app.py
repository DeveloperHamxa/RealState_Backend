from flask import Flask,jsonify, request,make_response
from flask_bcrypt import Bcrypt
from datetime import datetime
from realestate.config.db import db
import jwt
from datetime import datetime, timedelta
from functools import wraps
import bcrypt
from flask_jwt_extended import (JWTManager,
create_access_token,create_refresh_token,
get_jwt_identity,
jwt_required)

from realestate.controllers.addproperty import addproperty_blueprint
from realestate.controllers.searchproperty import searchproperty_blueprint
from realestate.controllers.allproperty import allproperty_blueprint



app = Flask(__name__)
bcrypt = Bcrypt(app)
secret ="*********"


app.register_blueprint(addproperty_blueprint, url_prefix="")
app.register_blueprint(searchproperty_blueprint, url_prefix="")
app.register_blueprint(allproperty_blueprint, url_prefix="")


@app.route('/signup', methods=['POST', 'GET'])
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
            data['password'] = bcrypt.generate_password_hash(
                data['password']).decode('utf-8')
            data['created'] = datetime.now()
            res = db["users"].insert_one(data)
            if res.acknowledged:
                message = "user created successfully"
                status = "successful"
    except Exception as ex:
        message = f"{ex}"
        status = "fail"
        code = 500
    return jsonify({'status': status, "message": message}), 200

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

@app.route('/login', methods=['POST', 'GET'])
def login():
    message = ""
    res_data = {}
    code = 500
    status = "fail"
    try:
        data = request.get_json()
        user = db["users"].find_one({"email": data["email"]})
        if user:
            user['_id'] = str(user['_id'])
            if user and bcrypt.check_password_hash(user['password'], data['password']):
                time = datetime.utcnow() + timedelta(hours=24)
                token = jwt.encode({
                    "user": {
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

@app.route('/refresh')
@jwt_required(refresh=True)
def post(self):

        current_user=get_jwt_identity()

        new_access_token=create_access_token(identity=current_user)

        return make_response(jsonify({"access_token":new_access_token}),200)

if __name__ == "__main__":
    app.run(debug=True)
