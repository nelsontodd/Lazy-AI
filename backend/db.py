from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.flask_db

assignments = db.assignments
assignments.create_index('name', unique=True)
users = db.users
users.create_index('email', unique=True)
