from pathlib import Path
from encryption import encrypt_data, load_key, decrypt_data

def load_image(image: Path) -> bytes:
    with open(image, 'rb') as f: return f.read()


def save_encrypted_image(image: Path, key: bytes):
    en_image_data = encrypt_data(load_image(image), key) # ENCRYPTED IMAGE
    global enc_image
    enc_image = str(image).split(".")[0] + ".bin"
    with open(enc_image, 'wb') as f:
        f.write(en_image_data)
    return enc_image


def save_decrypted_image(image: Path, key: bytes) -> bytes:
    dec_image = str(image).split(".")[0] + "_decrypted.jpg"
    print(dec_image)
    with open(dec_image, 'wb') as f:
        f.write(decrypt_data(load_image(enc_image), key))
    return dec_image