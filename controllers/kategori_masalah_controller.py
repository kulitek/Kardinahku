import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from sqlalchemy.orm import Session
from models import *
import bcrypt
from datetime import datetime, timedelta


def seed_kategori_masalah(db: Session):
    kategories_masalah = ['ringan','sedang','gawat','sangat gawat', 'darurat','bencana']
    if db is None:
        db = SessionLocal()
    try:
        for katmas in kategories_masalah:
            kategori_masalah = KategoriMasalah(kategori=katmas)
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
