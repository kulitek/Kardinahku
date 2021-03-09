import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from sqlalchemy.orm import Session
import models
import schemas.pegawai_schema  as schema
import bcrypt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def get_pegawai_by_id(db: Session, id: str):
    return db.query(models.Pegawai).filter(
        models.Pegawai.id == id,
        models.Pegawai.deleted_at == None,).first()

def get_pegawai_all(db: Session):
    return db.query(models.Pegawai).filter(
        models.Pegawai.deleted_at == None).all()


def seed_pegawai(db: Session):
    if db is None:
        db = SessionLocal()
    df = pd.read_csv('seed/DataPegawai.csv')
    df = df.astype(object)
    try:
        for i in range(0, df.shape[0]):
            pegawai = Pegawai(id=df.iloc[i]['IdPegawai'],
                              nama_lengkap=df.iloc[i]['NamaLengkap'],
                              nama_panggilan=df.iloc[i]['NamaPanggilan'],
                              jenis_kelamin=df.iloc[i]['JenisKelamin'],
                              tempat_lahir=df.iloc[i]['TempatLahir'],
                              tanggal_lahir=df.iloc[i]['TglLahir']
                             )
            db.add(pegawai)
            db.commit()
            db.refresh(pegawai)
    else:
        db.rollback()
    del df

def reset_pegawai(db: Session):
    try:
        db.query(Instalasi).delete()
        db.commit()
    else:
        db.rollback()

# def create_pegawai(db: Session, user: schema.UserRegister):
#     hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
#     db_user = models.Pegawai(username=user.username,
#                           password=hashed_password.decode('utf-8'),
#                           # password=hashed_password, # for instead of postgresql
#                           id_pegawai=user.id_pegawai,
#                           email=user.email)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def check_username_password(db: Session, user: schema.UserLogin):
#     db_user_info: models.Pegawai = get_user_by_username(db, username=user.username)
#     # print(db_user_info.password.decode('utf-8'))
#     return bcrypt.checkpw(user.password.encode('utf-8'), db_user_info.password.encode('utf-8'))
