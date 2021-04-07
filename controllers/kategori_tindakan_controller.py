import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from sqlalchemy.orm import Session
from models import KategoriTindakan
import bcrypt
from datetime import datetime, timedelta


def get_kategori_tindakan_all(db: Session):
    try:
        return db.query(KategoriTindakan).all()
    except Exception as e:
        print(e)
        return False

def seed_kategori_tindakan(db: Session):
    kategories_tindakan = ['pengecekan','penanganan','penanganan lanjut','perbaikan', 'perbaikan lanjut','penghapusan', 'pembuangan', 'penghancuran']
    if db is None:
        db = SessionLocal()
    try:
        for i, katmas in enumerate(kategories_tindakan):
            kategori_tindakan = KategoriTindakan(id=i+1,kategori=katmas)
            db.add(kategori_tindakan)
            db.commit()
            db.refresh(kategori_tindakan)
        return True
    except Exception as e:
        print(e)
        db.rollback()
        return False
    finally:
        del kategori_tindakan

def reset_kategori_tindakan(db: Session):
    try:
        db.query(KategoriTindakan).delete()
        db.commit()
        return True
    except Exception as e:
        print(e)
        db.rollback()
        return False
