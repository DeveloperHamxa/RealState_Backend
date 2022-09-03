
from flask import jsonify, request, Blueprint
from realestate.config.db import db
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, get_jwt,unset_jwt_cookies
)

addproperty_blueprint = Blueprint("addproperty", __name__)

@addproperty_blueprint.route('/addproperty', methods=['POST', "GET"])
def add_property():
    data = request.get_json()
    user_id = get_jwt_identity()
    print(user_id)
    res = db["estate"].insert_one(data, user_id)
    if res.acknowledged:
        message = "state created successfully"
        status = "successful"
        code = 201
        return jsonify({'status': status, "message": message}), code
    else:
        status = "unsuccessful"
        message = "Estate is not Created"
        code = 201
    return jsonify({'status': status, "message": message}), code
