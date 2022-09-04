from flask import jsonify, request, Blueprint
from realestate.config.db import db
import json
from bson import json_util

searchproperty_blueprint = Blueprint("searchproperty", __name__)


@searchproperty_blueprint.route('/property', methods=['POST', "GET"])
def search_property():
    data = request.get_json()
    estate_found = db['estate'].find_one(data)
    print(estate_found)
    if estate_found:
        message = "property found"
        status = "successful"
        code = 201
        output = {'name': estate_found['name'],'image': estate_found['image'],'location': estate_found['location'], 'area': estate_found['area'], 'price': estate_found['price']}
        page_sanitized = json.loads(json_util.dumps(output))
        return jsonify({'result': page_sanitized, 'status': status, "message": message}), code
    else:
        message = "not found"
        status = "unsuccessful"
        code = 201
        return jsonify({'status': status, "message": message}), code
