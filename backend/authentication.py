from datetime import datetime, timedelta
import jwt

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
    return data['id']
