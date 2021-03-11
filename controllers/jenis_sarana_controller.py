import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from sqlalchemy.orm import Session
from models import *
import bcrypt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def seed_jenis_sarana(db: Session):
    if db is None:
        db = SessionLocal()
    df = pd.read_csv('seed/JenisBarang.csv')
    df = df.astype(object)
    try:
        for i in range(0, df.shape[0]):
            jenis_sarana = JenisSarana(nama=df.iloc[i]['JenisBarang'])
            db.add(jenis_sarana)
            db.commit()
            db.refresh(jenis_sarana)
    except Exception:
        db.rollback()
    del df

def reset_jenis_sarana(db: Session):
    try:
        db.query(JenisSarana).delete()
        db.commit()
    except Exception:
        db.rollback()
