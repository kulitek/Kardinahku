import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from sqlalchemy.orm import Session
from models import *
import bcrypt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def seed_instalasi(db: Session):
    if db is None:
        db = SessionLocal()
    df = pd.read_csv('seed/Instalasi.csv')
    df = df.astype(object).where(pd.notnull(df), None)
    try:
        for i in range(0, df.shape[0]):
            instalasi = Instalasi(id=df.iloc[i]['KdInstalasi'],
                              nama=df.iloc[i]['NamaInstalasi'],
                             )
            db.add(instalasi)
            db.commit()
            db.refresh(instalasi)
        return True
    except Exception as e:
        print(e)
        db.rollback()
        return False
    finally:
        del df

def reset_instalasi(db: Session):
    try:
        db.query(Instalasi).delete()
        db.commit()
        return "All Instalasi have been deleted."
    except Exception as e:
        print(e)
        db.rollback()
        return "There's an error in reset_intalasi"

def get_instalasi(db: Session):
    try:
        return db.query(Instalasi).filter(Instalasi.deleted_at == None).all()
    except Exception as e:
        print(e)
        db.rollback()
        return None
