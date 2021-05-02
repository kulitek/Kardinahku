import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Masalah, User, Pegawai
from schemas.masalah_schema import *
import bcrypt, string, random
import pathlib as pl
from datetime import datetime, timedelta
import traceback

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
    try: pl.Path(r'{}'.format(old_name)).unlink()
    except Exception as e:
        print("masalah_controller put_file = " + traceback.format_exc())
        pass
    finally: return create_file(foto)

def get_masalah_by_deskripsi(db: Session, deskripsi: str):
    try:
        return db.query(Masalah).filter(
        Masalah.deskripsi == deskripsi,
        Masalah.deleted_at == None).first()
    except Exception as e:
        print(traceback.format_exc())
        db.rollback()
        return False

def get_masalah_all(db: Session, user):
    try:
        db_masalah = db.query(Masalah).filter(Masalah.deleted_at == None).all()
        for masalah in db_masalah:
            masalah.ruangan, masalah.kategori_masalah, masalah.sarana, masalah.tindakan, masalah.kategori_masalah
        return db_masalah
    except Exception as e:
        print('get_all_masalah',e)
        db.rollback()
        return False
    else:
        del db_masalah

def get_masalah_baru(db: Session, user):
    try:
        db_masalah = db.query(Masalah).filter(Masalah.deleted_at == None, Masalah.id_level_1 == None).all()
        for masalah in db_masalah:
            disposisi_1 = db.query(User).filter(User.deleted_at == None, User.id == masalah.id_level_1).first()
            setattr(masalah, 'disposisi_1', disposisi_1.pegawai if disposisi_1 else None)
            disposisi_2 = db.query(User).filter(User.deleted_at == None, User.id == masalah.id_level_2).first()
            setattr(masalah, 'disposisi_2', disposisi_2.pegawai if disposisi_2 else None)
            disposisi_3 = db.query(User).filter(User.deleted_at == None, User.id == masalah.id_level_3).first()
            setattr(masalah, 'disposisi_3', disposisi_3.pegawai if disposisi_3 else None)
            masalah.ruangan, masalah.kategori_masalah, masalah.sarana
        return [True, "sukses", db_masalah]
    except Exception as e:
        print('get_all_masalah ', traceback.format_exc())
        db.rollback()
        return [False, traceback.format_exc(), []]
    else: del db_masalah


def get_masalah_by_id(db: Session, id: int):
    try:
        db_masalah = db.query(Masalah).filter(Masalah.id == id, Masalah.deleted_at == None).first()
        disposisi_1 = db.query(User).filter(User.deleted_at == None, User.id == db_masalah.id_level_1).first()
        setattr(db_masalah, 'disposisi_1', disposisi_1.pegawai if disposisi_1 else None)
        disposisi_2 = db.query(User).filter(User.deleted_at == None, User.id == db_masalah.id_level_2).first()
        setattr(db_masalah, 'disposisi_2', disposisi_2.pegawai if disposisi_2 else None)
        disposisi_3 = db.query(User).filter(User.deleted_at == None, User.id == db_masalah.id_level_3).first()
        setattr(db_masalah, 'disposisi_3', disposisi_3.pegawai if disposisi_3 else None)
        db_masalah.ruangan, db_masalah.sarana, db_masalah.kategori_masalah
        return [True, "sukses", db_masalah]
    except Exception as e:
        print(traceback.format_exc())
        db.rollback()
        return [False, traceback.format_exc(), []]
    else:
        del db_masalah
        del disposisi_1
        del disposisi_2
        del disposisi_3


def get_masalah_by_disposisi_1(db: Session, id_disposisi_1: int):
    try:
        db_masalah = db.query(Masalah).filter(Masalah.id_level_1 == id_disposisi_1,
        Masalah.deleted_at == None, Masalah.id_level_2 == None, Masalah.id_level_3 == None).all()
        for masalah in db_masalah:
            disposisi_1 = db.query(User).filter(User.deleted_at == None, User.id == masalah.id_level_1).first()
            setattr(masalah, 'disposisi_1', disposisi_1.pegawai if disposisi_1 else None)
            disposisi_2 = db.query(User).filter(User.deleted_at == None, User.id == masalah.id_level_2).first()
            setattr(masalah, 'disposisi_2', disposisi_2.pegawai if disposisi_2 else None)
            disposisi_3 = db.query(User).filter(User.deleted_at == None, User.id == masalah.id_level_3).first()
            setattr(masalah, 'disposisi_3', disposisi_3.pegawai if disposisi_3 else None)
            masalah.ruangan, masalah.sarana, masalah.kategori_masalah
        return [True, "sukses", db_masalah]
    except Exception as e:
        print(traceback.format_exc())
        db.rollback()
        return [False, "gagal", []]
    else:
        del db_masalah
        del disposisi_1
        del disposisi_2
        del disposisi_3
def get_masalah_by_disposisi_2(db: Session, id_disposisi_2: int):
    try:
        db_masalah = db.query(Masalah).filter(Masalah.id_level_2 == id_disposisi_2,
        Masalah.deleted_at == None, Masalah.id_level_3 == None).all()
        for masalah in db_masalah:
            disposisi_1 = db.query(User).filter(User.deleted_at == None, User.id == masalah.id_level_1).first()
            setattr(masalah, 'disposisi_1', disposisi_1.pegawai if disposisi_1 else None)
            disposisi_2 = db.query(User).filter(User.deleted_at == None, User.id == masalah.id_level_2).first()
            setattr(masalah, 'disposisi_2', disposisi_2.pegawai if disposisi_2 else None)
            disposisi_3 = db.query(User).filter(User.deleted_at == None, User.id == masalah.id_level_3).first()
            setattr(masalah, 'disposisi_3', disposisi_3.pegawai if disposisi_3 else None)
            masalah.ruangan, masalah.sarana, masalah.kategori_masalah
        return [True, "sukses", db_masalah]
    except Exception as e:
        print(traceback.format_exc())
        db.rollback()
        return [False, "gagal", []]
    else:
        del db_masalah
        del disposisi_1
        del disposisi_2
        del disposisi_3
def get_masalah_by_disposisi_3(db: Session, id_disposisi_3: int):
    try:
        db_masalah = db.query(Masalah).filter(Masalah.id_level_3 == id_disposisi_3, Masalah.deleted_at == None,
        Masalah.id_level_1 != None, Masalah.id_level_2 != None).all()
        for masalah in db_masalah:
            disposisi_1 = db.query(User).filter(User.deleted_at == None, User.id == masalah.id_level_1).first()
            setattr(masalah, 'disposisi_1', disposisi_1.pegawai if disposisi_1 else None)
            disposisi_2 = db.query(User).filter(User.deleted_at == None, User.id == masalah.id_level_2).first()
            setattr(masalah, 'disposisi_2', disposisi_2.pegawai if disposisi_2 else None)
            disposisi_3 = db.query(User).filter(User.deleted_at == None, User.id == masalah.id_level_3).first()
            setattr(masalah, 'disposisi_3', disposisi_3.pegawai if disposisi_3 else None)
            masalah.ruangan, masalah.sarana, masalah.kategori_masalah
        return [True, "sukses", db_masalah]
    except Exception as e:
        print(traceback.format_exc())
        db.rollback()
        return [False, "gagal", []]
    else:
        del db_masalah
        del disposisi_1
        del disposisi_2
        del disposisi_3


def update_masalah_by_disposisi_1(db: Session, id_disposisi_1: int):
    return 0
def update_masalah_by_disposisi_2(db: Session, id_disposisi_2: int):
    return 0
def update_masalah_by_disposisi_3(db: Session, id_disposisi_3: int):
    return 0

def create_masalah(db: Session, masalah: MasalahCreate):
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
        disposisi_1 = db.query(User).filter(User.deleted_at == None, User.id == db_masalah.id_level_1).first()
        setattr(db_masalah, 'disposisi_1', disposisi_1.pegawai if disposisi_1 else None)
        disposisi_2 = db.query(User).filter(User.deleted_at == None, User.id == db_masalah.id_level_2).first()
        setattr(db_masalah, 'disposisi_2', disposisi_2.pegawai if disposisi_2 else None)
        disposisi_3 = db.query(User).filter(User.deleted_at == None, User.id == db_masalah.id_level_3).first()
        setattr(db_masalah, 'disposisi_3', disposisi_3.pegawai if disposisi_3 else None)
        return [True, "sukses", db_masalah]
    except Exception as e:
        print(traceback.format_exc())
        db.rollback()
        return [False, "gagal", []]


def update_masalah(db: Session, masalah: MasalahUpdate):
    db_masalah = db.query(Masalah).filter(Masalah.id == masalah.id, Masalah.deleted_at == None).first()
    if db_masalah:
        db_masalah.deskripsi = masalah.deskripsi if masalah.deskripsi else db_masalah.deskripsi
        db_masalah.id_ruangan = masalah.id_ruangan if masalah.id_ruangan else db_masalah.id_ruangan
        db_masalah.id_kategori_masalah = masalah.id_kategori_masalah if masalah.id_kategori_masalah else db_masalah.id_kategori_masalah
        db_masalah.id_sarana = masalah.id_sarana if masalah.id_sarana else db_masalah.id_sarana
        db_masalah.id_level_1 = masalah.id_level_1 if masalah.id_level_1 else db_masalah.id_level_1
        db_masalah.id_level_2 = masalah.id_level_2 if masalah.id_level_2 else db_masalah.id_level_2
        db_masalah.id_level_3 = masalah.id_level_3 if masalah.id_level_3 else db_masalah.id_level_3
        db_masalah.status = masalah.status if masalah.status else db_masalah.status
        db_masalah.done_at = datetime.now() if masalah.status else None
        db_masalah.foto = put_file(masalah.foto, db_masalah.foto) if masalah.foto else db_masalah.foto
        db_masalah.foto_selesai = put_file(masalah.foto_selesai, db_masalah.foto_selesai) if masalah.foto_selesai else db_masalah.foto_selesai
    else:
        return [True, "Masalah tidak ditemukan", db_masalah]
    try:
        db.commit()
        db.refresh(db_masalah)
        disposisi_1 = db.query(User).filter(User.deleted_at == None, User.id == db_masalah.id_level_1).first()
        setattr(db_masalah, 'disposisi_1', disposisi_1.pegawai if disposisi_1 else None)
        disposisi_2 = db.query(User).filter(User.deleted_at == None, User.id == db_masalah.id_level_2).first()
        setattr(db_masalah, 'disposisi_2', disposisi_2.pegawai if disposisi_2 else None)
        disposisi_3 = db.query(User).filter(User.deleted_at == None, User.id == db_masalah.id_level_3).first()
        setattr(db_masalah, 'disposisi_3', disposisi_3.pegawai if disposisi_3 else None)
        return [True, "sukses", db_masalah]
    except Exception as e:
        print(traceback.format_exc())
        db.rollback()
        return [False, "gagal", []]


def delete_masalah_by_id(db: Session, id: int):
    try:
        db_masalah = db.query(Masalah).filter(Masalah.id == id, Masalah.deleted_at == None).first()
        if db_masalah:
            db_masalah.deleted_at = datetime.now()
            db.commit()
            db.refresh(db_masalah)
            return [True, "sukses", db_masalah]
        else:
            return [False, "Masalah tidak ditemukan atau sudah dihapus.", []]
    except Exception as e:
        print(traceback.format_exc())
        db.rollback()
        return [False, "gagal", []]

def search_masalah(db: Session, key: str):
    try:
        db_masalah = db.query(Masalah).join(Masalah.ruangan).join(Masalah.kategori_masalah
                     ).join(Masalah.sarana).join(User).join(Pegawai).filter(or_(
            Masalah.deskripsi.ilike(r'%{}%'.format(key)),
            Masalah.kategori_masalah.property.mapper.class_.kategori.ilike(r'%{}%'.format(key)),
            Masalah.sarana.property.mapper.class_.nama.ilike(r'%{}%'.format(key)),
            Masalah.ruangan.property.mapper.class_.nama.ilike(r'%{}%'.format(key),),
            User.pegawai.property.mapper.class_.nama_lengkap.ilike(r'%{}%'.format(key)),

            Masalah.sarana.property.mapper.class_.nama.ilike(r'%{}%'.format(key)),
            Masalah.sarana.property.mapper.class_.nama.ilike(r'%{}%'.format(key)),
        ), Masalah.deleted_at == None)
        # masalah = db.query(Sarana).join()
        return [True, "sukses", db_masalah.all()]
    except Exception as e:
        print(traceback.format_exc())
        db.rollback()
        return [False, "gagal", []]

def search_masalah_by_disposisi(db: Session, key: str):
    try:
        db_masalah = db.query(Masalah)
    except Exception as e:
        print(traceback.format_exc())
        db.rollback()
        return [False, "gagal", []]
