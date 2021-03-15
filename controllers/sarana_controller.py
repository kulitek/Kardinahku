import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


import pathlib
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import *
from fastapi import UploadFile
import bcrypt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from schemas.sarana_schema import SaranaCreate


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

def put_file():
    global BASE_DIR
    return pathlib.Path.cwd() / 'assets' / 'sarana'

def create_sarana(db: Session, sarana: SaranaCreate):
    return None

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
