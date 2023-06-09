from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from marshmallow import ValidationError
from pymongo import MongoClient

from authentication import create_token
from schemas import LoginSchema, UserSchema
import utils
import constants
import lazy_ai


app = Flask(__name__)
CORS(app)

bcrypt = Bcrypt(app)

client = MongoClient('localhost', 27017)
db = client.flask_db
users = db.users
users.create_index('email', unique=True)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    schema = LoginSchema()
    try:
        result = schema.load(data)
        user = users.find_one({'email': data['email']})
        if user:
            password = data['password']
            if bcrypt.check_password_hash(user['password'], password):
                token = create_token(user)
                return jsonify({'token': token}), 200
            else:
                return jsonify(message="Invalid credentials."), 400
        else:
            return jsonify(message='This user does not exist.'), 400
    except ValidationError as err:
        return jsonify(message=err.messages), 400
    return jsonify(message="Server error"), 500

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    schema = UserSchema()
    try:
        result = schema.load(data)
        user = users.find_one({'email': data['email']})
        if user:
            return jsonify(message="This user already exists."), 400
        else:
            password = data['password']
            data['password'] = bcrypt.generate_password_hash(password)
            users.insert_one(data)
            return jsonify(message="User added!"), 200
    except ValidationError as err:
        return jsonify(message=err.messages), 400
    return jsonify(message="Server error"), 500

@app.route('/homework', methods=['POST'])
def create_solution():
    #TODO: Add security and schema validation logic
    #TODO: Get username, prompt for user full name, assignment description, title (optional)
    #Possibly: LLM Model selection
    data = request.files
    hwsolve = lazy_ai.LazyAI(data['file'].filename, "{} solutions".format(data['file'].filename), "Speech Language Pathology Exam Study Guide", "nelsontodd", "Nelson Morrow", "Homework 4")
    data['file'].save(hwsolve.input_rel_path(data['file'].filename))
    solutions = hwsolve.solutions_pdf()
    return jsonify(message="It works!")


if __name__ == '__main__':
    app.run(debug=True)
