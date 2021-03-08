import uvicorn
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, logger, Request, File, UploadFile, Form
from starlette import status
from typing import List, Any, Iterator
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.ext.sqlalchemy import paginate

import models
from datetime import datetime
from controllers.user_controller import *
from controllers.pegawai_controller import *
import schemas.user_schema as user_schema, schemas.pegawai_schema as pegawai_schema
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
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Authorization"}
    )
    try:
        token = request.headers["Authorization"]
        decoded_token = decode_access_token(data=token)
        username = decoded_token["sub"] if decoded_token["sub"] else None
    except (PyJWTError, KeyError):
        raise credentials_exception
    user = is_token(db=db, username=username, token=token)
    print(user)
    if user is None:
        raise credentials_exception
    return user

@app.post("/file/")
async def create_file(file: bytes = File(...)):
    # Thus use memory (RAM)
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": vars(file)}



@app.get("/pegawai", response_model=Page[pegawai_schema.Pegawai], dependencies=[Depends(pagination_params)])
def get_pegawai(db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return paginate(get_pegawai_all(db=db))


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
            return {"access_token": access_token,
                    "username": user.username}


@app.post("/login/form/", response_model=user_schema.Token)
def login_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = get_user_by_username(db=db, username=username)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Username tidak ditemukan.")
    else:
        user = user_schema.UserLogin(username=username, password=password)
        is_password_correct = check_username_password(db, user)
        if is_password_correct is False:
            raise HTTPException(status_code=400, detail="Password salah.")
        else:
            access_token = create_permanent_access_token(data={"sub": username}, db=db)
            return {"access_token": access_token,
                    "username": username}

@app.post("/register", response_model=user_schema.User)
def registering_user(user: user_schema.UserRegister, db: Session=Depends(get_db)):
    db_user = get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username sudah terpakai.")
    else:
        return create_user(db=db, user=user)
