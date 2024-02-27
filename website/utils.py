import os
import secrets
from hashlib import sha256 



def hash_and_salt_password(password, salt):
    hashed_and_salted_password = sha256((password + salt).encode()).hexdigest()
    return (hashed_and_salted_password)

def generate_salt():
    salt = secrets.token_hex(16)
    return salt
