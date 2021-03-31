import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from sqlalchemy.orm import Session
import models
import schemas.user_schema  as schema
import bcrypt
from fastapi import Depends, FastAPI, HTTPException, Request
from starlette import status
from typing import Any
from datetime import datetime, timedelta
from jwt import PyJWTError


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username,
        models.User.deleted_at == None).first()


def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(
        models.User.id == id,
        models.User.deleted_at == None,).first()


def create_user(db: Session, user: schema.UserRegister):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.User(username=user.username,
                          password=hashed_password.decode('utf-8'),
                          # password=hashed_password, # for instead of postgresql
                          id_pegawai=user.id_pegawai,
                          email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def check_username_password(db: Session, user: schema.UserLogin):
    db_user_info: models.User = get_user_by_username(db, username=user.username)
    # print(db_user_info.password.decode('utf-8'))
    return bcrypt.checkpw(user.password.encode('utf-8'), db_user_info.password.encode('utf-8'))


def reset_users(db):
    try:
        # db_users = db.query(models.User).all()
        db.query(models.User).delete()
        db.commit()
        return "Users deleted."
    except Exception as e:
        print(e)
        db.rollback()
        return e.with_traceback(sys.exc_info()[2])


def get_current_user_controller(request: Request, db: Session) -> Any:
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Could not validate credentials", headers = {"WWW-Authenticate": "Authorization"})
    token = None
    try:
        token = request.headers["Authorization"]
        decoded_token = decode_access_token(data=token)
        username = decoded_token["sub"] if decoded_token["sub"] else None
    except (PyJWTError, KeyError):
        raise credentials_exception
    user = is_token(db=db, username=username, token=token)
    if user is None:
        raise credentials_exception
    return user


import jwt

secret_key = "0943lds0o98icjo34kr39fucvoi3n4lkjrf09sd8iocjvl3k4t0f98dusj3kl"
algorithm = "HS256"


def create_access_token(*, data:dict, db: Session, expires_delta: timedelta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    db_user = get_user_by_username(db=db, username=str)
    db_user.token = encoded_jwt
    db.commit()
    db.refresh(db_user)
    return encoded_jwt

def is_token(db: Session, username: str, token: str):
    db_user = get_user_by_username(db=db, username=username)
    if db_user.token == token:
        return db_user
    else:
        return None


def decode_access_token(*, data: str):
    global secret_key, algorithm
    to_decode = data
    return jwt.decode(to_decode, secret_key, algorithms=algorithm)

def create_permanent_access_token(*, data: dict, db: Session):
    global secret_key
    encoded_jwt = jwt.encode(data, secret_key, algorithm=algorithm)
    db_user = get_user_by_username(db=db, username=data["sub"])
    db_user.token = encoded_jwt
    db.commit()
    db.refresh(db_user)
    return encoded_jwt


def check_token(db: Session, username: str, token: str):
    db_user: models.User = get_user_by_username(db, username=username)
    if db_user.token == token:
        return True
    else:
        return False
