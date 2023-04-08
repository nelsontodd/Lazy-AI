from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from marshmallow import ValidationError
from pymongo import MongoClient

from schemas import LoginSchema, UserSchema

app = Flask(__name__)
bcrypt = Bcrypt(app)

client = MongoClient('localhost', 27017)
db = client.flask_db
users = db.users

CORS(app)

@app.route('/', methods=['POST'])
def login():
    data = request.get_json()
    schema = LoginSchema()
    try:
        result = schema.load(data)
        raise
        password = data['password']
        data['password'] = bcrypt.generate_password_hash(password)
        users.insert_one(data)
    except ValidationError as err:
        return jsonify(message=err.messages), 400
    return jsonify(message="User added!"), 200

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    schema = UserSchema()
    try:
        result = schema.load(data)
        password = data['password']
        data['password'] = bcrypt.generate_password_hash(password)
        users.insert_one(data)
    except ValidationError as err:
        return jsonify(message=err.messages), 400
    return jsonify(message="User added!"), 200

if __name__ == '__main__':
    app.run(debug=True)
