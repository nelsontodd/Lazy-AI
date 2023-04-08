from datetime import datetime, timedelta
import jwt

def create_token(user):
    token = jwt.encode(
            {
                'id': str(user['_id']),
                'exp': datetime.utcnow() + timedelta(minutes=30)},
                'SECRET',
                'HS256'
            )
    return token
