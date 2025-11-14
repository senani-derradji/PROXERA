from cryptography.fernet import Fernet
import os
from validation import DataPayload

file_name = "fernet_key.key"

def generate_key_fernet():
    key = Fernet.generate_key()
    with open(file_name, "wb") as f: f.write(key)
    return key

def load_key():
    if os.path.exists(file_name):
        with open(file_name, "rb") as f: return f.read()
    else: return generate_key_fernet()

def encrypt_data(data: DataPayload, key: bytes) -> bytes:
    fer = Fernet(key)
    encrypted = fer.encrypt(data)
    return encrypted

def decrypt_data(encrypted_data: bytes, key: bytes) -> bytes:
    fer = Fernet(key)
    decrypted = fer.decrypt(encrypted_data)
    return decrypted