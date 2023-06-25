from bson.objectid import ObjectId
from flask import jsonify, request
from flask_bcrypt import Bcrypt
from jwt import ExpiredSignatureError
from marshmallow import ValidationError
from pymongo import MongoClient

from authentication import create_token, get_user
from schemas import FileSchema, LoginSchema, UserSchema
from db import insert_assignment, users
import utils
import constants
import lazy_ai

def register_routes(app):
    bcrypt = Bcrypt(app)

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

    @app.route('/homework/new', methods=['POST'])
    def create_solution():
        #TODO: Get username, prompt for user full name, assignment description, title (optional)
        #Possibly: LLM Model selection
        try:
            headers = request.headers
            if headers and  'x-auth-token' in headers:
                token = headers['x-auth-token']
                user = get_user(token)
                data = request.files
                file = data['file']
                if file is not None and user is not None:
                    result = FileSchema().load(file)
                    assignment_created = insert_assignment(user, file)
                    if assignment_created:
                        hwsolve = lazy_ai.LazyAI(
                            file.filename, "{} solutions".format(file.filename),
                            "Speech Language Pathology Exam Study Guide",
                            "nelsontodd",
                            "Nelson Morrow",
                            "Homework 4"
                        )
                        file.seek(0)
                        file.save(hwsolve.input_rel_path(file.filename))
                        solutions = hwsolve.solutions_pdf()
                        return jsonify(message="Assignment added."), 200
                    else:
                        return jsonify(
                                message="User already has an assignment with this name."
                                ), 400
                else:
                    return jsonify(message='User did not provide file.'), 400
            else:
                return jsonify(message='User is not logged in.'), 400
        except ExpiredSignatureError as error:
            return jsonify(message='User session expired.'), 400
        except ValidationError as err:
            return jsonify(message=err.messages), 400
        return jsonify(message="Server error"), 500
