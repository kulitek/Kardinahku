import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from sqlalchemy.orm import Session
from models import Masalah
from schemas.masalah_schema import *
import bcrypt
from datetime import datetime, timedelta

MASALAH_PATH = r'assets/masalah/'

def create_file(foto: UploadFile):
    global MASALAH_PATH
    new_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))
    file_type = ''.join([r'.',foto.filename.split(r'.')[-1]])
    new_name = new_name.replace(" ", r'-') + '__' + str(datetime.now().strftime(r'%Y%m%d%H%M%S')) + file_type
    pl.Path(r'{}{}'.format(MASALAH_PATH, new_name)).write_bytes(foto.file.read())
    foto.file.close()
    return r'{}{}'.format(MASALAH_PATH, new_name)

def put_file(foto: UploadFile, old_name):
    pl.Path(r'{}'.format(old_name)).unlink()
    return create_file(foto)

def get_masalah_by_deskripsi(db: Session, deskripsi: str):
    try:
        return db.query(Masalah).filter(
        Masalah.deskripsi == deskripsi,
        Masalah.deleted_at == None).first()
    except Exception as e:
        print(e)
        db.rollback()
        return False


def get_all_masalah(db: Session):
    try:
        db_masalah = db.query()
    except Exception as e:
        print('get_all_masalah',e)
        db.rollback()
        return False


def get_user_by_id(db: Session, id: int):
    try:
        return db.query(Masalah).filter(
        Masalah.id == id,
        Masalah.deleted_at == None,).first()
    except Exception as e:
        print(e)
        db.rollback()
        return False


def create_user(db: Session, masalah: MasalahCreate):
    db_masalah = Masalah(deskripsi=masalah.deskripsi,
                          id_user=masalah.id_user,
                          id_kategori_masalah=masalah.id_kategori_masalah,
                          id_ruangan=masalah.id_ruangan,
                          id_sarana=masalah.id_sarana)
    db_masalah.foto = create_file(masalah.foto) if masalah.foto else None
    try:
        db.add(db_masalah)
        db.commit()
        db.refresh(db_masalah)
        return db_masalah
    except Exception as e:
        print(e)
        db.rollback()
        return False


def update_masalah(db: Session, masalah: MasalahUpdate):
    db_masalah = db.query(Masalah).filter(Masalah.id == masalah.id, Masalah.deleted_at == None).first()
    db_masalah.deskripsi = masalah.deskripsi if masalah.deskripsi else db_masalah.deskripsi
    db_masalah.id_ruangan = masalah.id_ruangan if masalah.id_ruangan else db_masalah.id_ruangan
    db_masalah.id_kategori_masalah = masalah.id_kategori_masalah if masalah.id_kategori_masalah else db_masalah.id_kategori_masalah
    db_masalah.id_sarana = masalah.id_sarana if masalah.id_sarana else db_masalah.id_sarana
    db_masalah.status = masalah.status if masalah.status else db_masalah.status
    db_masalah.done_at = masalah.done_at if masalah.status else None
    db_masalah.foto = put_file(masalah.foto, db_masalah.foto) if masalah.foto else db_masalah.foto
    try:
        db.commit()
        db.refresh(db_masalah)
        return db_masalah
    except Exception as e:
        print(e)
        db.rollback()
        return False


def delete_masalah_by_id(db: Session, id: int):
    try:
        db_masalah = db.query(Masalah).filter(Masalah.id == id, Masalah.deleted_at == None).first()
        db_masalah.deleted_at = datetime.now()
        db.commit()
        db.refresh(db_sarana)
        return db_sarana
    except Exception as e:
        print(e)
        db.rollback()
        return False

def search_masalah(db: Session, key: str):
    try:
        db_masalah = db.query(Masalah).join(Masalah.ruangan).join(Masalah.kategori_masalah
                     ).join(Masalah.sarana).filter(or_(
            Masalah.deskripsi.ilike(r'%{}%'.format(key)),
            Masalah.kategori_masalah.property.mapper.class_.kategori.ilike(r'%{}%'.format(key)),
            Masalah.sarana.property.mapper.class_.nama.ilike(r'%{}%'.format(key)),
            Masalah.ruangan.property.mapper.class_.nama.ilike(r'%{}%'.format(key),)
        ), Sarana.deleted_at == None)
        # masalah = db.query(Sarana).join()
        return db_masalah.all()
    except Exception as e:
        print(e)
        db.rollback()
        return False
