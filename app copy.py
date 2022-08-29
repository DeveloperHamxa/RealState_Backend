from flask import Flask, render_template, jsonify,json, request
import pymongo
from pymongo import MongoClient
from user import routes
import re
from user import routes





app = Flask(__name__)


# client = pymongo.MongoClient('mongodb+srv://Hamxa:Hamxa.123@mydb.p3gucfo.mongodb.net/?retryWrites=true&w=majority')
# db = client["myDB"]
# users_collection = db["RealEstate"]
# print(client.list_database_names())


# print("Database is created !!")

# user = {
#         "_id": "",
#         "name": "name",
#         "email": 'email',
#         "password": "password",
#         }
# users_collection.insert_one(user)


@app.route('/', methods=['POST', 'GET'])
def register():
    name = request.json['name']
    email = request.json['email']

    user = User(
        name=name,
        email=email
        )

    db.session.add(user)
    db.session.commit()

    return article_schema.jsonify(article)


if __name__ == "__main__":
     app.run(debug=True ,port=8080,use_reloader=False)
