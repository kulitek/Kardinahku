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
    df = df.astype(object).where(pd.notnull(df), None)
    try:
        for i in range(0, df.shape[0]):
            jenis_sarana = JenisSarana(id=i+1,nama=df.iloc[i]['JenisBarang'])
            db.add(jenis_sarana)
            db.commit()
            db.refresh(jenis_sarana)
        return True
    except Exception as e:
        print(e)
        db.rollback()
        return False
    finally:
        del df

def reset_jenis_sarana(db: Session):
    try:
        db.query(JenisSarana).delete()
        db.commit()
        return True
    except Exception as e:
        print(e)
        db.rollback()
        return False

def get_jenis_sarana_all(db: Session):
    try:
        js = db.query(JenisSarana).filter(JenisSarana.deleted_at == None).all()
        return js
    except Exception as e:
        print(e)
        db.rollback()
        return None
