from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from pymongo import MongoClient

from controllers import register_routes
import utils
import constants
import lazy_ai


app = Flask(__name__)
CORS(app)
register_routes(app)


if __name__ == '__main__':
    app.run(debug=True)
