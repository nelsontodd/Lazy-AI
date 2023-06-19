from bson.objectid import ObjectId
from datetime import datetime, timedelta
import jwt

from db import users

def create_token(user):
    token = jwt.encode(
            {
                'id': str(user['_id']),
                'exp': datetime.utcnow() + timedelta(minutes=60)},
                'SECRET',
                'HS256'
            )
    return token

def decode_token(token):
    data = jwt.decode(jwt=token, key='SECRET', algorithms=['HS256'])
    return data

def get_user(token):
    user_id = decode_token(token)['id']
    user = users.find_one({'_id': ObjectId(user_id)})
    return user
