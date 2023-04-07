from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.flask_db
users = db.users

CORS(app)

@app.route('/hello', methods=['GET'])
def hello_world():
    users.insert_one({'name': 'Akhil', 'email': 'akhil4400@gmail.com'})
    return jsonify(message='Hello World!')

if __name__ == '__main__':
    app.run(debug=True)
