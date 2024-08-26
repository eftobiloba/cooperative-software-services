import secrets
import string

def generate_access_token(length=16):
    alphabet = string.ascii_letters + string.digits
    access_token = ''.join(secrets.choice(alphabet) for i in range(length))
    return access_token
