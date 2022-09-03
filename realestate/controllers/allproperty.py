from flask import jsonify, Blueprint
from realestate.config.db import db
from bson import json_util
import json


allproperty_blueprint = Blueprint("allproperty", __name__)


@allproperty_blueprint.route('/allproperty', methods=['GET', 'POST'])
def allproperty():
    data = db['estate'].find({}, {'name': 1, 'location': 1,'ptype': 1,'ftype': 1,'area': 1,'price': 1,'image': 1, '_id': 0})
    if data:
        message = "all property data"
        status = "successful"
        code = 201
        page_sanitized = json.loads(json_util.dumps(data))
        return jsonify({'result': page_sanitized, "message": message, "status": status})