import uvicorn
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, logger, Request
from starlette import status
from typing import List, Any, Iterator
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.ext.sqlalchemy import paginate

import models
from datetime import datetime
from controllers.user_controller import *
import schemas.user_scheme, schemas.pegawai_schema
from database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

async def get_current_user(request: Request, db: Session = Depends(get_db)) -> Any:
    token = request.headers["Authorization"]
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Authorization"}
    )
    try:
        decoded_token = decode_access_token(data=token)
        username = decoded_token["sub"] if decoded_token["sub"] else None
    except PyJWTError:
        raise credentials_exception
    user = is_token(db=db, username=username, token=token)
    if user is None:
        raise credentials_exception
    return user


@app.get("/pegawai", response_model=Page[pegawai_schema.PegawaiInfo], dependencies=[Depends(pagination_params)])
def get_pegawai(db: Session = Depends(get_db), current_user: user_scheme.User = Depends(get_current_user)):
    


@app.post("/login", response_model=user_schema.Token)
def login_user(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db=db, username=user.username)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Username tidak ditemukan.")
    else:
        is_password_correct = check_username_password(db, user)
        if is_password_correct is False:
            raise HTTPException(status_code=400, detail="Password salah.")
        else:
            access_token = create_permanent_access_token(data={"sub": user.username}, db=db)
            return {"access_token": access_token, "token_type": "normal"}

@app.post("/register", response_model=user_schema.User)
def registering_user(user: user_schema.UserRegister, db: Session=Depends(get_db)):
    db_user = get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username sudah terpakai.")
    else:
        return create_user(db=db, user=user)
