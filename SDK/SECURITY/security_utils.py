import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pathlib import Path
from SDK.validation import DataTypeValidate, DataTypes
from SDK.SECURITY.encryption import encrypt_data, decrypt_data


def load_data(data: Path) -> bytes:
    with open(data, 'rb') as f:
        return f.read()


def save_encrypted_data(image: DataTypeValidate, key: bytes):
    en_data_info = encrypt_data(load_data(image), key)
    enc_data = str(image).split(".")[0] + ".bin"
    with open(enc_data, 'wb') as f: f.write(en_data_info)
    return enc_data


def save_decrypted_image(image: Path, key: bytes, _type: DataTypes) -> bytes:
    dec_data = str(image).split(".")[0] + "_decrypted." + str(_type)
    dec_data_info = decrypt_data(load_data(image), key)
    with open(dec_data, 'wb') as f: f.write(dec_data_info)
    return dec_data