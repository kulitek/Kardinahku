import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import pathlib as pl
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import *
from fastapi import UploadFile
import bcrypt, string, random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from schemas.sarana_schema import SaranaCreate

SARANA_PATH = r'assets/sarana/'
# def seed_jenis_sarana(db: Session):
#     if db is None:
#         db = SessionLocal()
#     df = pd.read_csv('seed/JenisBarang.csv')
#     df = df.astype(object)
#     try:
#         for i in range(0, df.shape[0]):
#             jenis_sarana = JenisSarana(nama=df.iloc[i]['JenisBarang'])
#             db.add(jenis_sarana)
#             db.commit()
#             db.refresh(jenis_sarana)
#     except Exception:
#         db.rollback()
#     del df

def create_file(foto: UploadFile):
    global SARANA_PATH
    new_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))
    file_type = ''.join([r'.',foto.filename.split(r'.')[-1]])
    new_name = new_name.replace(" ", r'-') + '__' + str(datetime.now().strftime(r'%Y%m%d%H%M%S')) + file_type
    pl.Path(r'{}{}'.format(SARANA_PATH, new_name)).write_bytes(foto.file.read())
    foto.file.close()
    return r'{}{}'.format(SARANA_PATH, new_name)

def put_file(foto: UploadFile, old_name):
    global SARANA_PATH
    # new_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))
    file_type = ''.join([r'.',foto.filename.split(r'.')[-1]])
    new_name = new_name.replace(" ", r'-') + '__' + str(datetime.now().strftime(r'%Y%m%d%H%M%S')) + file_type
    pl.Path(r'{}{}'.format(SARANA_PATH, new_name)).write_bytes(foto.file.read())
    foto.file.close()
    return r'{}{}'.format(SARANA_PATH, new_name)

def create_sarana(db: Session, sarana: SaranaCreate):
    db_sarana = Sarana(nama=sarana.nama,id_ruangan=sarana.id_ruangan,id_jenis=sarana.id_jenis)
    db_sarana.foto = create_file(sarana.foto)
    try:
        db.add(db_sarana)
        db.commit()
        db.refresh(db_sarana)
        return db_sarana
    except Exception as e:
        print(e)
        db.rollback()
        return e

def reset_sarana(db: Session):
    try:
        db.query(Sarana).delete()
        db.commit()
    except Exception:
        db.rollback()



def search_sarana(db: Session, key: str):
    try:
        db.query(Sarana).filter(or_(
            Sarana.nama.like(key),
            Sarana.berat.like(key),
            Sarana.panjang.like(key),
            Sarana.tinggi.like(key),
        )).all()
    except Exception as e:
        print(e)
        db.rollback()
