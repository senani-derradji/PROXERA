import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from SDK.DBS.models import File
from SDK.SECURITY.sensetive import KeysEncryption


enc_dec = KeysEncryption()


def create_file_record(db : Session,
                       file_id,
                       file_name,
                       file_type,
                       file_length,
                       file_path,
                       action = None
                       ):

    file = File(file_id=enc_dec.key_for_db('enc',(str(file_id).encode())),
                file_name=enc_dec.key_for_db('enc',str(file_name).encode()),
                file_type=file_type,
                file_length=file_length,
                file_path=enc_dec.key_for_db('enc',str(file_path).encode()),
                action=action
                )
    db.add(file)
    db.commit()
    db.refresh(file)
    return file

def get_file_by_id(db: Session, id_) -> str:
    if not id_: return None
    id_ = db.query(File).filter(File.id == id_).first()
    if id_.file_id:
        return id_.file_id
    else: return None


def get_all_files(db: Session):
    return db.query(File).all()

def delete_file_by_id(db: Session, file_id):
    db.query(File).filter(File.file_id == enc_dec.key_for_db('dec',file_id).decode()).delete()
    db.commit()
    return True

def get_data_type_by_id(db: Session, file_id):
    row = db.query(File).filter(File.file_id == file_id).first()
    print(row)
    return row.file_type if row else exit()


