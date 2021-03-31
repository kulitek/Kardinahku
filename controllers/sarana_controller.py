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
from schemas.sarana_schema import SaranaCreate, SaranaUpdate

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

def get_sarana_all(db: Session):
    try:
        return db.query(Sarana).filter(Sarana.deleted_at == None).all()
    except Exception as e:
        print(e)
        return False

def create_file(foto: UploadFile):
    global SARANA_PATH
    new_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))
    file_type = ''.join([r'.',foto.filename.split(r'.')[-1]])
    new_name = new_name.replace(" ", r'-') + '__' + str(datetime.now().strftime(r'%Y%m%d%H%M%S')) + file_type
    pl.Path(r'{}{}'.format(SARANA_PATH, new_name)).write_bytes(foto.file.read())
    foto.file.close()
    return r'{}{}'.format(SARANA_PATH, new_name)

def put_file(foto: UploadFile, old_name):
    pl.Path(r'{}'.format(old_name)).unlink()
    return create_file(foto)

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
        return False

def update_sarana(db: Session, sarana: SaranaUpdate):
    db_sarana = db.query(Sarana).filter(Sarana.id == sarana.id, Sarana.deleted_at == None).first()
    db_sarana.nama = sarana.nama if sarana.nama else db_sarana.nama
    db_sarana.id_ruangan = sarana.id_ruangan if sarana.id_ruangan else db_sarana.id_ruangan
    db_sarana.id_jenis = sarana.id_jenis if sarana.id_jenis else db_sarana.id_jenis
    db_sarana.berat = sarana.berat if sarana.berat else db_sarana.berat
    db_sarana.panjang = sarana.panjang if sarana.panjang else db_sarana.panjang
    db_sarana.lebar = sarana.lebar if sarana.lebar else db_sarana.lebar
    db_sarana.tinggi = sarana.tinggi if sarana.tinggi else db_sarana.tinggi
    db_sarana.foto = put_file(sarana.foto, db_sarana.foto) if sarana.foto else db_sarana.foto
    try:
        db.commit()
        db.refresh(db_sarana)
        return db_sarana
    except Exception as e:
        print(e)
        db.rollback()
        return False

async def delete_sarana(db: Session, id: int):
    try:
        db_sarana = db.query(Sarana).filter(Sarana.id == id, Sarana.deleted_at == None).first()
        db_sarana.deleted_at = datetime.now()
        db.commit()
        db.refresh(db_sarana)
        return db_sarana
    except Exception as e:
        print(e)
        db.rollback()
        return False
    else:
        del db_sarana

def reset_sarana(db: Session):
    try:
        db.query(Sarana).delete()
        db.commit()
        return "All Sarana have been deleted."
    except Exception as e:
        print(e)
        db.rollback()
        return "There's an error on function reset_sarana"



def search_sarana(db: Session, key: str):
    try:
        sarana = db.query(Sarana).join(Sarana.ruangan).join(Sarana.jenis).filter(or_(
            Sarana.nama.ilike(r'%{}%'.format(key)),
            Sarana.jenis.property.mapper.class_.nama.ilike(r'%{}%'.format(key)),
            Sarana.ruangan.property.mapper.class_.nama.ilike(r'%{}%'.format(key),)
        ), Sarana.deleted_at == None)
        # sarana = db.query(Sarana).join()
        return sarana.all()
    except Exception as e:
        print(e)
        db.rollback()
        return False
