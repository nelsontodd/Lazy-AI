import json
import os
import sys

import clamd
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
CORS(app, resources={r"/homework": {"origins": ["https://homeworkhero.io"]}})

client = Client(
    access_token=os.environ['SQUARE_ACCESS_TOKEN'],
    environment='sandbox'
)

@app.route('/homework', methods=['POST'])
def create_solution():
    print('create_solution')
    #TODO: Get username, prompt for user full name, assignment description, title (optional)
    #Possibly: LLM Model selection
    try:
        file = request.files['file']
        has_latex = utils.convert_str_to_bool(request.form['hasLatex'])
        assignment_type = request.form['assignmentType'].upper()
        email = request.form['email']
        name = request.form['name']
        token = request.form['sourceId']
        title = request.form['title']
        print('Email: {}'.format(email))
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
                cd = clamd.ClamdNetworkSocket()
                cd.__init__(host='localhost', port=3310, timeout=None)
                scan_result = cd.instream(file)
                if scan_result['stream'][0] == 'OK':
                    file.seek(0)
                    result = FileSchema().load(file)
                    print(f"Got file {file.filename}", file=sys.stderr)
                    uuid = str(uuid4())
                    hwsolve = lazy_ai.LazyAI(
                                file.filename,
                                "{} solutions".format(file.filename),
                                "", uuid, name,
                                document_title=title,
                                latex=has_latex,
                                assignment_type=assignment_type
                            )
                    file.seek(0)
                    file.save(hwsolve.input_rel_path(file.filename))
                    cost = hwsolve.determine_cost() #Based on token count/OCR fees
                    print(f"Cost for this file {file.filename} will be {cost}", file=sys.stderr)
                    solutions = '{}.pdf'.format(hwsolve.solutions_pdf())
                    print(f"Retrieved solutions.", file=sys.stderr)
                    return send_file(solutions)
                else:
                    return jsonify(message='File has a virus.'), 400
            elif create_payment_response.is_error():
                return jsonify(message='Payment error.'), 400
        else:
            return jsonify(message='User did not provide file.'), 400
    except ValidationError as err:
        return jsonify(message=err.messages), 400
    return jsonify(message="Server error"), 500


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
