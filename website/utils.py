import os
import hashlib



def hash_and_salt_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    salt = os.urandom(32)
    return (hashed_password, salt)
