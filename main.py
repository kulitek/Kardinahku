import uvicorn
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, logger, Request, File, UploadFile, Form, Response
from starlette import status
from typing import List, Any, Iterator, Optional
from urllib.parse import quote
# from fastapi_pagination import Page, add_pagination, paginate

import models, string, random
import pathlib as pl
from datetime import datetime
from controllers.user_controller import *
from controllers.pegawai_controller import *
from controllers.ruangan_controller import *
from controllers.jenis_sarana_controller import *
from controllers.instalasi_controller import *
from controllers.sarana_controller import *
import schemas.user_schema as user_schema, schemas.pegawai_schema as pegawai_schema
from schemas.instalasi_schema import InstalasiGetAll
from schemas.sarana_schema import SaranaCreate, SaranaUpdate
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


@app.post("/file")
async def get_file(path: str):
    # Thus use memory (RAM)
    # path = quote(path)
    img = None
    try:
        img = pl.Path(path).resolve().read_bytes()
        extension = path.split(r'.')[-1]
        media_type = "image/png" if r'.png' in extension else "image/jpeg"
        return Response(content=img, media_type=media_type)
    except Exception as e:
        return {r'error': str(e)}
    else:
        img = None
        extension = None
        media_type = None

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    new_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))
    file_type = ''.join([r'.',file.filename.split(r'.')[-1]])
    new_name = new_name.replace(" ", r'-') + '__' + str(datetime.now().strftime(r'%Y%m%d%H%M%S')) + file_type
    pats = pl.Path(r'assets/sarana/{}'.format(new_name)).write_bytes(file.file.read())
    file.file.close()
    img = pl.Path(r'assets/sarana/{}'.format(new_name)).read_bytes()
    # return {"filename": pl.Path(r'assets/sarana/{}'.format(file.filename)).resolve(),
    #         "file": ''}
    return Response(content=img, media_type=file.content_type)

@app.delete("/users")
def api_reset_users(db: Session = Depends(get_db)):
    return {"status": True, "message": "Sukses", "data": reset_users(db=db)}


@app.get("/pegawai")
def app_get_pegawai(db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": get_pegawai_all(db=db)}
@app.get("/pegawai/{id}")
def app_get_pegawai(id: str, db: Session = Depends(get_db),current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": get_pegawai_by_id(db=db,id=id)}
@app.post("/pegawai")
def get_pegawai(nama: str = Form(...), db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": get_pegawai_by_nama(db=db, nama=nama)}
@app.post("/pegawai/seed")
def app_seed_pegawai(db: Session = Depends(get_db), code: str = Form(...)):
    if code == 'utuhmbak':
        return {"status": True, "message": "sukses", "data": seed_pegawai(db=db)}
    else:
        raise HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Code not valid.",
        headers = {"WWW-Authenticate": "Authorization"})

@app.delete("/pegawai/reset")
def app_reset_pegawai(db: Session = Depends(get_db), code: str = Form(...)):
    if code == 'utuhmbak':
        return {"status": True, "message": "sukses", "data": reset_pegawai(db=db)}
    else:
        raise HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Code not valid.",
        headers = {"WWW-Authenticate": "Authorization"})

@app.get("/ruangan")
def app_get_ruangan(db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": get_ruangan(db=db)}

@app.get("/instalasi")
def app_get_instalasi(db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": get_instalasi(db=db)}

@app.get("/jenissarana")
def app_get_jenissarana(db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": get_jenis_sarana_all(db=db)}

@app.post("/sarana")
def app_create_sarana(nama: str = Form(...), id_ruangan: int = Form(...),
                id_jenis: int = Form(...), foto: Optional[UploadFile] = File(None),
                current_user: user_schema.User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    sarana = SaranaCreate(nama=nama,id_ruangan=id_ruangan,id_jenis=id_jenis,foto=foto)
    return {"status": True, "message": "sukses", "data": create_sarana(db=db,sarana=sarana)}
@app.put("/sarana")
def app_update_sarana(id: int = Form(...), nama: Optional[str] = Form(None), id_ruangan: Optional[int] = Form(None),
                berat: Optional[str] = Form(None), panjang: Optional[str] = Form(None), tinggi: Optional[str] = Form(None), lebar: Optional[str] = Form(None),
                id_jenis: Optional[int] = Form(None), foto: Optional[UploadFile] = File(None),
                # current_user: user_schema.User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    sarana = SaranaUpdate(id=id,nama=nama,id_ruangan=id_ruangan,id_jenis=id_jenis,
                          berat=berat,panjang=panjang,tinggi=tinggi,lebar=lebar)
    sarana.foto = foto if foto else None
    return {"status": True, "message": "sukses", "data": update_sarana(db=db,sarana=sarana)}
@app.delete("/sarana/{id}")
async def delete_sarana_id(id: str, db: Session = Depends(get_db)):
    return {"status": True, "message": "sukses", "data": await delete_sarana(db=db, id=id)}
@app.get("/sarana")
async def app_get_sarana_all(db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": get_sarana_all(db=db)}
@app.get("/sarana/{key}")
async def app_search_sarana(key: str, db: Session = Depends(get_db),
                            # current_user: user_schema.User = Depends(get_current_user)
                            ):
    return {"status": True, "message": "sukses", "data": search_sarana(db=db,key=key)}

# @app.get("/percobaan")
# def percobaan():
#     return {"status": True, "message": "sukses", "data": put_file()}

@app.post("/login")
def app_login_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
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
                    user_schema.UserRegistered(username=username,api_token=access_token))}

@app.post("/register")
def app_registering_user(username: str = Form(...), password: str = Form(...),
                     email: str = Form(...), id_pegawai: str = Form(...),
                     db: Session=Depends(get_db)):
    user = user_schema.UserRegister(username=username, password=password,email=email, id_pegawai=id_pegawai)
    db_user = get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username sudah terpakai.")
    else:
        return {"status": True, "message": "sukses", "data": create_user(db=db, user=user)}
