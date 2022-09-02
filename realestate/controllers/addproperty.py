
from flask import jsonify, request, Blueprint
from realestate.config.db import db

addproperty_blueprint = Blueprint("addproperty", __name__)



@addproperty_blueprint.route('/addproperty', methods=['POST', "GET"])
def add_property():
    data = request.get_json()
    res = db["estate"].insert_one(data)
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
