import bcrypt
from .models import Admin, Volunteer, Client


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





    