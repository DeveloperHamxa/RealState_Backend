
import pymongo


client = pymongo.MongoClient('mongodb+srv://Hamxa:Hamxa.123@mydb.p3gucfo.mongodb.net/?retryWrites=true&w=majority')
db = client["myDB"]
users_collection = db["RealEstate"]
print(client.list_database_names())