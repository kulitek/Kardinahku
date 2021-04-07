import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Masalah, User, Pegawai, Tindakan
from schemas.tindakan_schema import *
import bcrypt, string, random
import pathlib as pl
from datetime import datetime, timedelta

TINDAKAN_PATH = r'assets/tindakan/'

def create_file(foto: UploadFile):
    global TINDAKAN_PATH
    new_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))
    file_type = ''.join([r'.',foto.filename.split(r'.')[-1]])
    new_name = new_name.replace(" ", r'-') + '__' + str(datetime.now().strftime(r'%Y%m%d%H%M%S')) + file_type
    pl.Path(r'{}{}'.format(TINDAKAN_PATH, new_name)).write_bytes(foto.file.read())
    foto.file.close()
    return r'{}{}'.format(TINDAKAN_PATH, new_name)

def put_file(foto: UploadFile, old_name):
    pl.Path(r'{}'.format(old_name)).unlink()
    return create_file(foto)

def get_tindakan_by_kondisi(db: Session, deskripsi: str):
    try:
        return db.query(Tindakan).filter(
        Tindakan.kondisi_awal == deskripsi,
        Tindakan.tindakan == deskripsi,
        Tindakan.kondisi_pasca == deskripsi,
        Tindakan.deleted_at == None).first()
    except Exception as e:
        print(e)
        db.rollback()
        return False


def get_tindakan_all(db: Session):
    try:
        return db.query(Tindakan).filter(Tindakan.deleted_at == None).all()
    except Exception as e:
        print('get_all_tindakan',e)
        db.rollback()
        return False


def get_tindakan_by_id(db: Session, id: int):
    try:
        db_tindakan = db.query(Tindakan).filter(Tindakan.id == id, Tindakan.deleted_at == None).first()
        disposisi_1 = db.query(User).filter(User.deleted_at == None, User.id == db_tindakan.id_level_1).first()
        setattr(db_tindakan, 'disposisi_1', disposisi_1.pegawai if disposisi_1 else None)
        disposisi_2 = db.query(User).filter(User.deleted_at == None, User.id == db_tindakan.id_level_2).first()
        setattr(db_tindakan, 'disposisi_2', disposisi_2.pegawai if disposisi_2 else None)
        disposisi_3 = db.query(User).filter(User.deleted_at == None, User.id == db_tindakan.id_level_3).first()
        setattr(db_tindakan, 'disposisi_3', disposisi_3.pegawai if disposisi_3 else None)
        return [True, "sukses", db_tindakan]
    except Exception as e:
        print(e)
        db.rollback()
        return [False, "gagal", []]
    # finally:
    #     del db_tindakan
    #     del disposisi_1
    #     del disposisi_2
    #     del disposisi_3


def create_tindakan(db: Session, tindakan: TindakanCreate):
    db_tindakan = Tindakan(kondisi_awal=tindakan.kondisi_awal,
                          tindakan=tindakan.tindakan,
                          kondisi_pasca=tindakan.kondisi_pasca,
                          id_user=tindakan.id_user,
                          id_masalah=tindakan.id_masalah,
                          id_kategori=tindakan.id_kategori,
                          id_ruangan=tindakan.id_ruangan,
                          id_sarana=tindakan.id_sarana)
    db_tindakan.foto = create_file(tindakan.foto) if tindakan.foto else None
    try:
        db.add(db_tindakan)
        db.commit()
        db.refresh(db_tindakan)
        return [True, "sukses", db_tindakan]
    except Exception as e:
        print(e)
        db.rollback()
        return [False, "gagal", []]


def update_tindakan(db: Session, tindakan: TindakanUpdate):
    db_tindakan = db.query(Tindakan).filter(Tindakan.id == tindakan.id, Tindakan.deleted_at == None).first()
    db_tindakan.kondisi_awal = tindakan.kondisi_awal if tindakan.kondisi_awal else db_tindakan.kondisi_awal
    db_tindakan.tindakan = tindakan.tindakan if tindakan.tindakan else db_tindakan.tindakan
    db_tindakan.kondisi_pasca = tindakan.kondisi_pasca if tindakan.kondisi_pasca else db_tindakan.kondisi_pasca
    db_tindakan.id_masalah = tindakan.id_masalah if tindakan.id_masalah else db_tindakan.id_masalah
    db_tindakan.id_ruangan = tindakan.id_ruangan if tindakan.id_ruangan else db_tindakan.id_ruangan
    db_tindakan.id_kategori = tindakan.id_kategori if tindakan.id_kategori else db_tindakan.id_kategori
    db_tindakan.id_sarana = tindakan.id_sarana if tindakan.id_sarana else db_tindakan.id_sarana
    db_tindakan.done_at = datetime.now() if tindakan.status else None
    db_tindakan.foto = put_file(tindakan.foto, db_tindakan.foto) if tindakan.foto else db_tindakan.foto
    try:
        db.commit()
        db.refresh(db_tindakan)
        return [True, "sukses", db_tindakan]
    except Exception as e:
        print(e)
        db.rollback()
        return [False, "gagal", []]


def delete_tindakan_by_id(db: Session, id: int):
    try:
        db_tindakan = db.query(Tindakan).filter(Tindakan.id == id, Tindakan.deleted_at == None).first()
        if db_tindakan:
            db_tindakan.deleted_at = datetime.now()
            db.commit()
            db.refresh(db_tindakan)
            return [True, "sukses", db_tindakan]
        else:
            return [False, "tindakan sudah dihapus", []]
    except Exception as e:
        print(e)
        db.rollback()
        return [False, "gagal", []]

def search_tindakan(db: Session, key: str):
    try:
        db_tindakan = db.query(Tindakan).join(Tindakan.ruangan).join(Tindakan.kategori_tindakan
                     ).join(Tindakan.sarana).join(User).join(Pegawai).filter(or_(
            Tindakan.kondisi_awal.ilike(r'%{}%'.format(key)),
            Tindakan.kategori_tindakan.property.mapper.class_.kategori.ilike(r'%{}%'.format(key)),
            Tindakan.sarana.property.mapper.class_.nama.ilike(r'%{}%'.format(key)),
            Tindakan.ruangan.property.mapper.class_.nama.ilike(r'%{}%'.format(key),),
            User.pegawai.property.mapper.class_.nama_lengkap.ilike(r'%{}%'.format(key)),

            Tindakan.sarana.property.mapper.class_.nama.ilike(r'%{}%'.format(key)),
            Tindakan.sarana.property.mapper.class_.nama.ilike(r'%{}%'.format(key)),
        ), Tindakan.deleted_at == None)
        # tindakan = db.query(Sarana).join()
        return [True, "sukses", db_tindakan.all()]
    except Exception as e:
        print(e)
        db.rollback()
        return [False, "gagal", []]

def search_tindakan_by_disposisi(db: Session, key: str):
    try:
        db_tindakan = db.query(Tindakan)
    except Exception as e:
        print(e)
        db.rollback()
        return [False, "gagal", []]
