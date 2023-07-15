from bson.objectid import ObjectId
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
from jwt import ExpiredSignatureError
from marshmallow import ValidationError
from pymongo import MongoClient

from authentication import create_token, get_user
from schemas import FileSchema, LoginSchema, UserSchema
from db import assignments, users
import utils
import constants
import lazy_ai


app = Flask(__name__)
CORS(app)

@app.route('/homework', methods=['POST'])
def create_solution():
    #TODO: Get username, prompt for user full name, assignment description, title (optional)
    #Possibly: LLM Model selection
    try:
        file = request.files['file']
        if file is not None:
            result = FileSchema().load(file)
            hwsolve = lazy_ai.LazyAI(
                file.filename, "{} solutions".format(file.filename),
                "Speech Language Pathology Exam Study Guide",
                "nelsontodd",
                "Nelson Morrow",
                "Homework 4"
            )
            file.seek(0)
            file.save(hwsolve.input_rel_path(file.filename))
            solutions = '{}.pdf'.format(hwsolve.solutions_pdf())
            print('Solutions: ', solutions)
            return send_file(solutions)
        else:
            return jsonify(message='User did not provide file.'), 400
    except ValidationError as err:
        return jsonify(message=err.messages), 400
    return jsonify(message="Server error"), 500


if __name__ == '__main__':
    app.run(debug=True)
