import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from sqlalchemy.orm import Session
from models import *
import bcrypt
from datetime import datetime, timedelta


jenis_sarana = ['elektronik','sedang','gawat','sangat gawat', 'darurat','bencana']

def seed_kategori_masalah(db: Session):
    global jenis_sarana
    if db is None:
        db = SessionLocal()
    try:
        for katmas in jenis_sarana:
            kategori_masalah = KategoriMasalah(kategori=katmas)
            db.add(kategori_masalah)
            db.commit()
            db.refresh(kategori_masalah)
    except:
        db.rollback()

def reset_kategori_masalah(db: Session):
    try:
        db.query(KategoriMasalah).delete()
        db.commit()
    except Exception:
        db.rollback()
