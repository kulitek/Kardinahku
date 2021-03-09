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
    df = df.astype(object)
    try:
        for i in range(0, df.shape[0]):
            instalasi = Instalasi(id=df.iloc[i]['KdInstalasi'],
                              nama=df.iloc[i]['NamaInstalasi'],
                             )
            db.add(instalasi)
            db.commit()
            db.refresh(instalasi)
    else:
        db.rollback()
    del df

def reset_instalasi(db: Session):
    try:
        db.query(Instalasi).delete()
        db.commit()
    else:
        db.rollback()
