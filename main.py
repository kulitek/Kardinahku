import uvicorn
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, logger, Request, File, UploadFile, Form
from starlette import status
from typing import List, Any, Iterator
# from fastapi_pagination import Page, add_pagination, paginate

import models
from datetime import datetime
from controllers.user_controller import *
from controllers.pegawai_controller import *
from controllers.ruangan_controller import *
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
    token = None
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



# @app.get("/pegawai", response_model=Page[pegawai_schema.Pegawai])
# def get_pegawai(db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
#     return paginate(get_pegawai_all(db=db))

@app.get("/pegawai")
def get_pegawai(db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": get_pegawai_all(db=db)}

@app.get("/pegawai/{nama}")
def get_pegawai(nama: str, db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": get_pegawai_by_nama(db=db, nama=nama)}

@app.get("/ruangan")
def get_pegawai(db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": get_ruangan(db=db)}


@app.post("/login")
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
            return {"status": True, "message": "sukses", "data": vars(
                    user_schema.UserRegistered(username=username,api_token=access_token)
            )}

@app.post("/register")
def registering_user(username: str = Form(...), password: str = Form(...),
                     email: str = Form(...), id_pegawai: str = Form(...),
                     db: Session=Depends(get_db)):
    user = user_schema.UserRegister(username=username, password=password,email=email, id_pegawai=id_pegawai)
    db_user = get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username sudah terpakai.")
    else:
        return {"status": True, "message": "sukses", "data": create_user(db=db, user=user)}
