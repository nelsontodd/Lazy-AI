import json
import os

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from marshmallow import ValidationError
from square.client import Client
from uuid import uuid4

from schemas import FileSchema
import utils
import constants
import lazy_ai


app = Flask(__name__)
CORS(app)

client = Client(
    access_token=os.environ['SQUARE_ACCESS_TOKEN'],
    environment='sandbox'
)


@app.route('/homework', methods=['POST'])
def create_solution():
    #TODO: Get username, prompt for user full name, assignment description, title (optional)
    #Possibly: LLM Model selection
    try:
        file = request.files['file']
        has_latex = request.form['hasLatex']
        is_homework = request.form['isHomework']
        name = request.form['name']
        token = request.form['sourceId']
        title = request.form['title']
        if file is not None and token is not None:
            create_payment_response = client.payments.create_payment(
                body={
                    'source_id': token,
                    'idempotency_key': str(uuid4()),
                    'amount_money': {
                        'amount': 100, # $1.00 charge
                        'currency': 'USD',
                    },
                }
            )
            if create_payment_response.is_success():
                result = FileSchema().load(file)
                hwsolve = lazy_ai.LazyAI(
                        file.filename, "{} solutions".format(file.filename),
                        "Speech Language Pathology Exam Study Guide",
                        "nelsontodd",
                        name,
                        title,
                        )
                file.seek(0)
                file.save(hwsolve.input_rel_path(file.filename))
                solutions = '{}.pdf'.format(hwsolve.solutions_pdf())
                return send_file(solutions)
            elif create_payment_response.is_error():
                return jsonify(message='Payment error.'), 400
        else:
            return jsonify(message='User did not provide file.'), 400
    except ValidationError as err:
        return jsonify(message=err.messages), 400
    return jsonify(message="Server error"), 500


if __name__ == '__main__':
    app.run(debug=True)
