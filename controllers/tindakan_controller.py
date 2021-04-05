import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Masalah, User, Pegawai, Tindakan
from schemas.masalah_schema import *
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

def get_tindakan_by_deskripsi(db: Session, deskripsi: str):
    try:
        return db.query(Masalah).filter(
        Masalah.deskripsi == deskripsi,
        Masalah.deleted_at == None).first()
    except Exception as e:
        print(e)
        db.rollback()
        return False


def get_tindakan_all(db: Session):
    try:
        return db.query(Masalah).filter(Masalah.deleted_at == None).all()
    except Exception as e:
        print('get_all_tindakan',e)
        db.rollback()
        return False


def get_tindakan_by_id(db: Session, id: int):
    try:
        db_tindakan = db.query(Masalah).filter(Masalah.id == id, Masalah.deleted_at == None).first()
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


def create_tindakan(db: Session, masalah: MasalahCreate):
    db_tindakan = Masalah(deskripsi=masalah.deskripsi,
                          id_user=masalah.id_user,
                          id_kategori_tindakan=masalah.id_kategori_tindakan,
                          id_ruangan=masalah.id_ruangan,
                          id_sarana=masalah.id_sarana)
    db_tindakan.foto = create_file(masalah.foto) if masalah.foto else None
    try:
        db.add(db_tindakan)
        db.commit()
        db.refresh(db_tindakan)
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


def update_tindakan(db: Session, masalah: MasalahUpdate):
    db_tindakan = db.query(Masalah).filter(Masalah.id == masalah.id, Masalah.deleted_at == None).first()
    db_tindakan.deskripsi = masalah.deskripsi if masalah.deskripsi else db_tindakan.deskripsi
    db_tindakan.id_ruangan = masalah.id_ruangan if masalah.id_ruangan else db_tindakan.id_ruangan
    db_tindakan.id_kategori_tindakan = masalah.id_kategori_tindakan if masalah.id_kategori_tindakan else db_tindakan.id_kategori_tindakan
    db_tindakan.id_sarana = masalah.id_sarana if masalah.id_sarana else db_tindakan.id_sarana
    db_tindakan.id_level_1 = masalah.id_level_1 if masalah.id_level_1 else db_tindakan.id_level_1
    db_tindakan.id_level_2 = masalah.id_level_2 if masalah.id_level_2 else db_tindakan.id_level_2
    db_tindakan.id_level_3 = masalah.id_level_3 if masalah.id_level_3 else db_tindakan.id_level_3
    db_tindakan.status = masalah.status if masalah.status else db_tindakan.status
    db_tindakan.done_at = masalah.done_at if masalah.status else None
    db_tindakan.foto = put_file(masalah.foto, db_tindakan.foto) if masalah.foto else db_tindakan.foto
    try:
        db.commit()
        db.refresh(db_tindakan)
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


def delete_tindakan_by_id(db: Session, id: int):
    try:
        db_tindakan = db.query(Masalah).filter(Masalah.id == id, Masalah.deleted_at == None).first()
        if db_tindakan:
            db_tindakan.deleted_at = datetime.now()
            db.commit()
            db.refresh(db_tindakan)
            return [True, "sukses", db_tindakan]
        else:
            return [False, "masalah sudah dihapus", []]
    except Exception as e:
        print(e)
        db.rollback()
        return [False, "gagal", []]

def search_tindakan(db: Session, key: str):
    try:
        db_tindakan = db.query(Masalah).join(Masalah.ruangan).join(Masalah.kategori_tindakan
                     ).join(Masalah.sarana).join(User).join(Pegawai).filter(or_(
            Masalah.deskripsi.ilike(r'%{}%'.format(key)),
            Masalah.kategori_tindakan.property.mapper.class_.kategori.ilike(r'%{}%'.format(key)),
            Masalah.sarana.property.mapper.class_.nama.ilike(r'%{}%'.format(key)),
            Masalah.ruangan.property.mapper.class_.nama.ilike(r'%{}%'.format(key),),
            User.pegawai.property.mapper.class_.nama_lengkap.ilike(r'%{}%'.format(key)),

            Masalah.sarana.property.mapper.class_.nama.ilike(r'%{}%'.format(key)),
            Masalah.sarana.property.mapper.class_.nama.ilike(r'%{}%'.format(key)),
        ), Masalah.deleted_at == None)
        # masalah = db.query(Sarana).join()
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
