import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from sqlalchemy.orm import Session
from models import KategoriMasalah
import bcrypt
from datetime import datetime, timedelta


def get_kategori_masalah_all(db: Session):
    try:
        return db.query(KategoriMasalah).all()
    except Exception as e:
        print(e)
        return False

def seed_kategori_masalah(db: Session):
    kategories_masalah = ['ringan','sedang','gawat','sangat gawat', 'darurat','bencana']
    if db is None:
        db = SessionLocal()
    try:
        for i, katmas in enumerate(kategories_masalah):
            kategori_masalah = KategoriMasalah(id=i+1,kategori=katmas)
            db.add(kategori_masalah)
            db.commit()
            db.refresh(kategori_masalah)
        return True
    except Exception as e:
        print(e)
        db.rollback()
        return False
    finally:
        del kategori_masalah

def reset_kategori_masalah(db: Session):
    try:
        db.query(KategoriMasalah).delete()
        db.commit()
        return True
    except Exception as e:
        print(e)
        db.rollback()
        return False
