import dropbox, os, keyring
from pathlib import Path
from SDK.UTILS.general_utils import PathManager
from SDK.SERVICES.logs_service import logger
from SDK.UTILS.general_utils import get_os_type
from SDK.UTILS.general_utils import save_large_data, load_large_data
from cryptography.fernet import Fernet



_KEY = "DATA_DROP_KEY"
_TOKEN_SYS_NAME = "TOKEN_DROP"
_SERVICE = f"Crypteria{get_os_type()}"


if keyring.get_password(f"Crypteria{get_os_type()}",_KEY) is None:
    k = keyring.set_password(
                            f"Crypteria{get_os_type()}",
                            _KEY,
                            Fernet.generate_key().decode()
                             )

else: k = keyring.get_password(f"Crypteria{get_os_type()}",_KEY)

fer = Fernet(k)


def authenticate():

    token = load_large_data(_SERVICE, _TOKEN_SYS_NAME)

    if token is None:
        print('''
        GO TP : https://www.dropbox.com/developers/apps
        CREATE NEW APP || OPEN EXISTING APP
        SETTINGS ---> GENERATE ACCESS TOKEN ---> GENERATE
              ''')

        token_user = input("DROPBOX ACCESS TOKEN: ").strip()
        enc_token = fer.encrypt(token_user.encode())

        save = save_large_data(_SERVICE, _TOKEN_SYS_NAME, enc_token.decode())

        dec_tok = load_large_data(_SERVICE, _TOKEN_SYS_NAME)
        dec_token = fer.decrypt(dec_tok)

    else: dec_token = fer.decrypt(token)

    return dec_token


ACCESS_TOKEN = authenticate().decode()
dbx = dropbox.Dropbox(ACCESS_TOKEN)


def upload_file(local_path, dropbox_path=None):
    if dropbox_path is None: dropbox_path = f"/{Path(local_path).name}"

    try:
        with open(local_path, "rb") as f:
            global result
            result = dbx.files_upload(f.read(), dropbox_path, mute=True)
    except Exception as e:
        logger.error(f"Dropbox Upload Error: {e}")
        exit()

    file_id = result.id
    logger.info(f"Dropbox Upload Successful — File ID: {file_id}")

    return file_id



def list_files(folder_path=""):

    response = dbx.files_list_folder(folder_path)

    files = []
    for entry in response.entries:
        if isinstance(entry, dropbox.files.FileMetadata):
            item = {
                "name": entry.name,
                "id": entry.id,
                "path": entry.path_lower
            }
            files.append(item)
            logger.info(f"{entry.name}  (ID: {entry.id})  PATH: {entry.path_lower}")

    return files



def download_file(file_path_or_id):

    if file_path_or_id.startswith("id:"):
        metadata = dbx.files_get_metadata(file_path_or_id)
        dropbox_path = metadata.path_lower

    else:
        dropbox_path = file_path_or_id

    file_name = Path(dropbox_path).name
    local_path = PathManager.get_temp_folder("CrypteriaBin") / file_name

    metadata, res = dbx.files_download(path=dropbox_path)

    with open(local_path, "wb") as f: f.write(res.content)

    logger.info(f"Dropbox Download Successful: {local_path}")

    return local_path