from pathlib import Path
from encryption import encrypt_data, decrypt_data
from validation import DataTypeValidate, DataTypes


def load_image(image: Path) -> bytes:
    with open(image, 'rb') as f:
        return f.read()


def save_encrypted_image(image: DataTypeValidate, key: bytes):

    en_image_data = encrypt_data(load_image(image), key)
    enc_image = str(image).split(".")[0] + ".bin"

    with open(enc_image, 'wb') as f: f.write(en_image_data)

    return enc_image


def save_decrypted_image(image: Path, key: bytes, _type: DataTypes) -> bytes:

    dec_image = str(image).split(".")[0] + "_decrypted." + str(_type)

    with open(dec_image, 'wb') as f: f.write(decrypt_data(load_image(image), key))

    return dec_image



def get_length_of_file(file: Path) -> int: return str(len(load_image(file)))

def get_type_of_file(file: Path) -> str: return str(file).split(".")[1]

def get_name_of_file(file: Path) -> str: return str(file).split(".")[0]

def get_path_of_file(file: Path) -> str: return str(file)