import bcrypt
from .models import Admin, Volunteer, Client
import jwt
import datetime
from decouple import config


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def check_password(hashed_password: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def check_unique_email(email: str) -> bool:
    try:
        Admin.objects.get(email = email)
        return False
    except Admin.DoesNotExist:
        try:
            Volunteer.objects.get(email = email)
            return False
        except Volunteer.DoesNotExist:
            try:
                Client.objects.get(email = email)
                return False
            except Client.DoesNotExist:
                return True
            


def generate_jwt(role, user_id):
    secret_key = config("SECRET_KEY_JWT")
    payload = {
        'user_id': user_id,
        'role' : role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=int(config("TOKEN_EXPIRY_TIME"))),
    }
    
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


def decode_jwt(token):
    secret_key = config("SECRET_KEY_JWT")
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return "Token has expired"
    except jwt.InvalidTokenError:
        return "Invalid token"
    
def admin_access(token):
    if not token:
        return False
    decoded = decode_jwt(token)
    if isinstance(decoded, str):
        return False
    if decoded.get('role') != 'admin':
        return False
    return True

def volunteer_access(token):
    if not token:
        return False
    decoded = decode_jwt(token)
    if isinstance(decoded, str):
        return False
    if decoded.get('role') not in ['admin','volunteer']:
        return False
    return True

def client_access(token):
    if not token:
        return False
    decoded = decode_jwt(token)
    if isinstance(decoded, str):
        return False
    if decoded.get('role') not in ['admin','client']:
        return False
    return True






    