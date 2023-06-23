from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.flask_db

assignments = db.assignments
users = db.users
users.create_index('email', unique=True)


def insert_assignment(user, file):
    filename = file.filename
    user_id = user['_id']
    assignment = assignments.find_one(
        {'user_id': user_id, 'name': filename}
    )
    if assignment:
        return False
    else:
        assignments.insert_one(
            {'name': file.filename, 'user_id': user_id}
        )
        return True
