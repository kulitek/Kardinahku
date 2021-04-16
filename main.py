import uvicorn
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, logger, Request, File, UploadFile, Form, Response
from starlette import status as sts
from typing import List, Any, Iterator, Optional
from urllib.parse import quote
import traceback
# from fastapi_pagination import Page, add_pagination, paginate

import models, string, random
import pathlib as pl
from datetime import datetime
from utils.imageutil import return_image
from controllers.user_controller import *
from controllers.pegawai_controller import *
from controllers.ruangan_controller import *
from controllers.jenis_sarana_controller import *
from controllers.instalasi_controller import *
from controllers.sarana_controller import *
from controllers.kategori_masalah_controller import *
from controllers.kategori_tindakan_controller import *
from controllers.masalah_controller import *
from controllers.tindakan_controller import *
import schemas.user_schema as user_schema, schemas.pegawai_schema as pegawai_schema
from schemas.instalasi_schema import InstalasiGetAll
from schemas.sarana_schema import SaranaCreate, SaranaUpdate
from schemas.masalah_schema import MasalahCreate, MasalahUpdate
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
    return get_current_user_controller(request=request, db=db)
async def get_current_admin(request: Request, db: Session = Depends(get_db)) -> Any:
    return role_checker_admin(request=request, db=db)
async def get_current_sub_admin(request: Request, db: Session = Depends(get_db)) -> Any:
    return role_checker_sub_admin(request=request, db=db)
async def get_current_operator(request: Request, db: Session = Depends(get_db)) -> Any:
    return role_checker_operator(request=request, db=db)


@app.get("/file/assets/sarana/{filename}")
async def get_file(filename: str):
    return return_image(SARANA_PATH, filename)
@app.get("/file/assets/masalah/{filename}")
async def get_file(filename: str):
    return return_image(MASALAH_PATH, filename)
# @app.get("/file/assets/tindakan/{filename}")
# async def get_file(filename: str):
#     return return_image(SARANA_PATH, filename)


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


# ============================== User ============================== #
@app.get("/users")
def api_get_all_users(db: Session = Depends(get_db)):
    try: return {"status": True, "message": "sukses", "data": get_all_users(db=db)}
    except Exception: return {"status": True, "message": traceback.format_exc(), "data": []}
@app.get("/users/current")
def api_get_all_users(db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):

    try: return {"status": True, "message": "sukses", "data": {"id": current_user.id, "username": current_user.username, "role": current_user.role}}
    except Exception: return {"status": True, "message": traceback.format_exc(), "data": ""}
@app.post("/users/role/{id}")
def api_update_role_by_id(id: int, db: Session = Depends(get_db), code: str = Form(...), # current_user: user_schema.User = Depends(get_current_super_admin),
role: str = Form(...)):
    if code == 'utuhmbak':
        try:
            response = update_user_role_by_id(db=db,id=id,role=role)
            return {"status": response[0], "message": response[1], "data": response[2]}
        except Exception: return {"status": True, "message": traceback.format_exc(), "data": []}
        else: del response
    else: return {"status": False,"message": "code invalid."}
@app.delete("/users")
def api_reset_users(db: Session = Depends(get_db), code: str = Form(...)):
    if code == 'utuhmbak':
        return {"status": True, "message": "Sukses", "data": reset_users(db=db)}
    else:
        raise HTTPException(status_code = sts.HTTP_401_UNAUTHORIZED, detail = "Code not valid.")
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
                    user_schema.UserRegistered(username=username,api_token=access_token,role=db_user.role))}
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


# ============================== Pegawai ============================== #
@app.get("/pegawai")
def app_get_pegawai(db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": get_pegawai_all(db=db)}
@app.get("/pegawai/{id}")
def app_get_pegawai(id: str, db: Session = Depends(get_db),current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": get_pegawai_by_id(db=db,id=id)}
@app.post("/pegawai")
def get_pegawai(nama: str = Form(...), db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": get_pegawai_by_nama(db=db, nama=nama)}
@app.post("/pegawai/seed/")
def app_seed_pegawai(db: Session = Depends(get_db), code: str = Form(...)):
    if code == 'utuhmbak':
        return {"status": True, "message": "sukses", "data": seed_pegawai(db=db)}
    else:
        raise HTTPException(status_code = sts.HTTP_401_UNAUTHORIZED, detail = "Code not valid.")
@app.delete("/pegawai/reset/")
def app_reset_pegawai(db: Session = Depends(get_db), code: str = Form(...)):
    if code == 'utuhmbak':
        return {"status": True, "message": "sukses", "data": reset_pegawai(db=db)}
    else:
        raise HTTPException(status_code = sts.HTTP_401_UNAUTHORIZED, detail = "Code not valid.")


# ============================== Ruangan ============================== #
@app.get("/ruangan")
def app_get_ruangan(db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": get_ruangan(db=db)}
@app.post("/ruangan/seed")
def app_seed_ruangan(db: Session = Depends(get_db), code: str = Form(...)):
    if code == 'utuhmbak':
        return {"status": True, "message": "sukses", "data": seed_ruangan(db=db)}
    else:
        raise HTTPException(status_code = sts.HTTP_423_LOCKED, detail = "Code not valid.")
@app.delete("/ruangan/reset/")
def app_reset_ruangan(db: Session = Depends(get_db), code: str = Form(...)):
    if code == 'utuhmbak':
        return {"status": True, "message": "sukses", "data": reset_ruangan(db=db)}
    else:
        raise HTTPException(status_code = sts.HTTP_423_LOCKED, detail = "Code not valid.")


# ============================== Instalasi ============================== #
@app.get("/instalasi")
def app_get_instalasi(db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": get_instalasi(db=db)}
@app.post("/instalasi/seed")
def app_seed_instalasi(db: Session = Depends(get_db), code: str = Form(...)):
    if code == 'utuhmbak':
        return {"status": True, "message": "sukses", "data": seed_instalasi(db=db)}
    else:
        raise HTTPException(status_code = sts.HTTP_401_UNAUTHORIZED, detail = "Code not valid.")
@app.delete("/instalasi/reset/")
def app_reset_instalasi(db: Session = Depends(get_db), code: str = Form(...)):
    if code == 'utuhmbak':
        return {"status": True, "message": "sukses", "data": reset_instalasi(db=db)}
    else:
        raise HTTPException(status_code = sts.HTTP_401_UNAUTHORIZED, detail = "Code not valid.")


# ============================== Jenis Sarana / jenis_sarana ============================== #
@app.get("/jenissarana")
def app_get_jenis_sarana(db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": get_jenis_sarana_all(db=db)}
@app.post("/jenissarana/seed/")
def app_seed_jenis_sarana(db: Session = Depends(get_db), code: str = Form(...)):
    if code == 'utuhmbak':
        return {"status": True, "message": "sukses", "data": seed_jenis_sarana(db=db)}
    else:
        raise HTTPException(status_code = sts.HTTP_401_UNAUTHORIZED, detail = "Code not valid.")
@app.delete("/jenissarana/reset/")
def app_reset_jenis_sarana(db: Session = Depends(get_db), code: str = Form(...)):
    if code == 'utuhmbak':
        return {"status": True, "message": "sukses", "data": reset_jenis_sarana(db=db)}
    else:
        raise HTTPException(status_code = sts.HTTP_401_UNAUTHORIZED, detail = "Code not valid.")


# ============================== Sarana ============================== #
@app.post("/sarana")
def app_create_sarana(nama: str = Form(...), id_ruangan: int = Form(...),
                id_jenis: int = Form(...), foto: Optional[UploadFile] = File(None),
                current_user: user_schema.User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    try:
        sarana = SaranaCreate(nama=nama,id_ruangan=id_ruangan,id_jenis=id_jenis,foto=foto)
    except Exception as e:
        raise HTTPException(detail="Error = " + str(e))
    return {"status": True, "message": "sukses", "data": create_sarana(db=db,sarana=sarana)}
@app.put("/sarana")
def app_update_sarana(id: int = Form(...), nama: Optional[str] = Form(None), id_ruangan: Optional[int] = Form(None),
                berat: Optional[str] = Form(None), panjang: Optional[str] = Form(None), tinggi: Optional[str] = Form(None), lebar: Optional[str] = Form(None),
                id_jenis: Optional[int] = Form(None), foto: Optional[UploadFile] = File(None),
                current_user: user_schema.User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    sarana = SaranaUpdate(id=id,nama=nama,id_ruangan=id_ruangan,id_jenis=id_jenis,
                          berat=berat,panjang=panjang,tinggi=tinggi,lebar=lebar)
    sarana.foto = foto if foto else None
    return {"status": True, "message": "sukses", "data": update_sarana(db=db,sarana=sarana)}
@app.delete("/sarana/{id}")
async def delete_sarana_id(id: str, db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": await delete_sarana(db=db, id=id)}
@app.get("/sarana")
async def app_get_sarana_all(db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": get_sarana_all(db=db)}
@app.get("/sarana/id/{id}")
async def app_get_sarana_with_id(id: int, db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": get_sarana_by_id(db=db, id=id)}
@app.get("/sarana/{key}")
async def app_search_sarana(key: str, db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": search_sarana(db=db,key=key)}
# @app.post("/sarana/seed")
# def app_seed_sarana(db: Session = Depends(get_db), code: str = Form(...)):
#     if code == 'utuhmbak':
#         return {"status": True, "message": "sukses", "data": seed_sarana(db=db)}
#     else:
#         raise HTTPException(status_code = sts.HTTP_401_UNAUTHORIZED, detail = "Code not valid.")
@app.delete("/sarana/reset/")
def app_reset_sarana(db: Session = Depends(get_db), code: str = Form(...)):
    if code == 'utuhmbak':
        return {"status": True, "message": "sukses", "data": reset_sarana(db=db)}
    else:
        raise HTTPException(status_code = sts.HTTP_401_UNAUTHORIZED, detail = "Code not valid.")


# ============================== Kategori Masalah ============================== #
@app.get("/kategorimasalah")
def app_get_kategori_masalah(db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": get_kategori_masalah_all(db=db)}
@app.post("/kategorimasalah/seed/")
def app_seed_kategori_masalah(db: Session = Depends(get_db), code: str = Form(...)):
    if code == 'utuhmbak':
        return {"status": True, "message": "sukses", "data": seed_kategori_masalah(db=db)}
    else:
        raise HTTPException(status_code = sts.HTTP_401_UNAUTHORIZED, detail = "Code not valid.")
@app.delete("/kategorimasalah/reset/")
def app_reset_kategori_masalah(db: Session = Depends(get_db), code: str = Form(...)):
    if code == 'utuhmbak':
        return {"status": True, "message": "sukses", "data": reset_kategori_masalah(db=db)}
    else:
        raise HTTPException(status_code = sts.HTTP_401_UNAUTHORIZED, detail = "Code not valid.")


# ============================== Masalah ============================== #
@app.get("/masalah")
def app_get_masalah(db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user),):
    try: return {"status": True, "message": "sukses", "data": get_masalah_all(db=db, user=current_user)}
    except Exception as e: return {"status": False, "message": "Error: " + traceback.format_exc(), "data": []}
@app.get("/masalah/disposisi_1/{disposisi_1}")
def app_get_masalah_disposisi_1(disposisi_1: int, db: Session = Depends(get_db),
current_user: user_schema.User = Depends(get_current_admin)):
    response = get_masalah_by_disposisi_1(db=db, id_disposisi_1=disposisi_1)
    try: return {"status": response[0], "message": response[1], "data": response[2]}
    except Exception as e: return {"status": False, "message": "Error: " + str(e), "data": []}
    else: del response
@app.get("/masalah/disposisi_2/{disposisi_2}")
def app_get_masalah_disposisi_2(disposisi_2: int, db: Session = Depends(get_db),
current_user: user_schema.User = Depends(get_current_sub_admin)):
    response = get_masalah_by_disposisi_2(db=db, id_disposisi_2=disposisi_2)
    try: return {"status": response[0], "message": response[1], "data": response[2]}
    except Exception as e: return {"status": False, "message": "Error: " + str(e), "data": []}
    else: del response
@app.get("/masalah/disposisi_3/{disposisi_3}")
def app_get_masalah_disposisi_3(disposisi_3: int, db: Session = Depends(get_db),
current_user: user_schema.User = Depends(get_current_operator)):
    response = get_masalah_by_disposisi_3(db=db, id_disposisi_3=disposisi_3)
    try: return {"status": response[0], "message": response[1], "data": response[2]}
    except Exception as e: return {"status": False, "message": "Error: " + str(e), "data": []}
    else: del response
@app.post("/masalah/disposisi_1/{disposisi_1}")
def app_update_masalah_disposisi_1(disposisi_1: int, db: Session = Depends(get_db),
current_user: user_schema.User = Depends(get_current_admin)):
    try: return {"status": True, "message": "sukses", "data": update_masalah_by_disposisi_1(db=db, id_disposisi_1=disposisi_1)}
    except Exception as e: return {"status": False, "message": "Error: " + str(e), "data": []}
@app.post("/masalah/disposisi_2/{disposisi_2}")
def app_update_masalah_disposisi_2(disposisi_2: int, db: Session = Depends(get_db),
current_user: user_schema.User = Depends(get_current_admin)):
    try: return {"status": True, "message": "sukses", "data": update_masalah_by_disposisi_2(db=db, id_disposisi_2=disposisi_2)}
    except Exception as e: return {"status": False, "message": "Error: " + str(e), "data": []}
@app.post("/masalah/disposisi_3/{disposisi_3}")
def app_update_masalah_disposisi_3(disposisi_3: int, db: Session = Depends(get_db),
current_user: user_schema.User = Depends(get_current_sub_admin)):
    try: return {"status": True, "message": "sukses", "data": update_masalah_by_disposisi_3(db=db, id_disposisi_3=disposisi_3)}
    except Exception as e: return {"status": False, "message": "Error: " + str(e), "data": []}
@app.post("/masalah")
def app_create_masalah(deskripsi: str = Form(...), id_ruangan: int = Form(...), id_sarana: int = Form(...),
                id_kategori_masalah: int = Form(...), foto: Optional[UploadFile] = File(None),
                current_user: user_schema.User = Depends(get_current_user), # id_user: int = Form(...),
                db: Session = Depends(get_db)):
    response = None
    try:
        masalah = MasalahCreate(deskripsi=deskripsi,id_user=current_user.id, id_sarana=id_sarana,
        id_kategori_masalah=id_kategori_masalah,id_ruangan=id_ruangan,foto=foto)
        response = create_masalah(db=db,masalah=masalah)
        del masalah
        return {"status": response[0], "message": response[1], "data": response[2]}
    except Exception as e: raise HTTPException(status_code = sts.HTTP_410_GONE,detail="Error = " + str(e))
    finally: del response
@app.put("/masalah/{id}")
def app_update_masalah(id: int, deskripsi: Optional[str] = Form(None), id_ruangan: Optional[int] = Form(None),
                id_level_1: Optional[int] = Form(None), id_level_2: Optional[int] = Form(None),
                id_level_3: Optional[int] = Form(None), id_sarana: Optional[int] = Form(None),
                id_kategori_masalah: Optional[int] = Form(None), foto: Optional[UploadFile] = File(None),
                status: Optional[bool] = Form(None), # id_user: int = Form(None),
                current_user: user_schema.User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    response = None
    try:
        masalah = MasalahUpdate(id=id,deskripsi=deskripsi, id_sarana=id_sarana,
        id_level_1=id_level_1, id_level_2=id_level_2, id_level_3=id_level_3, status=status,
        id_kategori_masalah=id_kategori_masalah,id_ruangan=id_ruangan,foto=foto)
        response = update_masalah(db=db,masalah=masalah)
        del masalah
        return {"status": response[0], "message": response[1], "data": response[2]}
    except Exception as e: raise HTTPException(status_code = sts.HTTP_410_GONE,detail="Error = " + str(e))
    finally: del response
@app.delete("/masalah/{id}")
async def delete_masalah_id(id: str, db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    response = None
    try:
        response = delete_masalah_by_id(db=db, id=id)
        return {"status": response[0], "message": response[1], "data": response[2]}
    except Exception as e: return {"status": False, "message": "Error: " + str(e), "data": []}
    finally: del response
@app.get("/masalah/{key}")
async def search_masalah_flexible(key: str, db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    response = None
    try:
        response = search_masalah(db=db, key=key)
        return {"status": response[0], "message": response[1], "data": response[2]}
    except Exception as e: return {"status": False, "message": "gagal", "data": []}
    finally: del response
@app.get("/masalah/id/{id}")
async def get_masalah_id(id: int, db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    response = None
    try:
        response = get_masalah_by_id(db=db, id=id)
        return {"status": response[0], "message": response[1], "data": response[2]}
    except Exception as e: return {"status": False, "message": "gagal", "data": []}
    finally: del response




# ============================== Kategori Tindakan ============================== #
@app.get("/kategoritindakan")
def app_get_kategori_tindakan(db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return {"status": True, "message": "sukses", "data": get_kategori_tindakan_all(db=db)}
@app.post("/kategoritindakan/seed/")
def app_seed_kategori_tindakan(db: Session = Depends(get_db), code: str = Form(...)):
    if code == 'utuhmbak':
        return {"status": True, "message": "sukses", "data": seed_kategori_tindakan(db=db)}
    else:
        raise HTTPException(status_code = sts.HTTP_401_UNAUTHORIZED, detail = "Code not valid.")
@app.delete("/kategoritindakan/reset/")
def app_reset_kategori_tindakan(db: Session = Depends(get_db), code: str = Form(...)):
    if code == 'utuhmbak':
        return {"status": True, "message": "sukses", "data": reset_kategori_tindakan(db=db)}
    else:
        raise HTTPException(status_code = sts.HTTP_401_UNAUTHORIZED, detail = "Code not valid.")




# ============================== Tindakan ============================== #
@app.get("/tindakan")
def app_get_tindakan(db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user),):
    return {"status": True, "message": "sukses", "data": get_tindakan_all(db=db)}
@app.get("/tindakan/{key}")
def app_search_tindakan(key: str, db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user),):
    return {"status": True, "message": "sukses", "data": search_tindakan(db=db, key=key)}
@app.get("/tindakan/id/{id}")
def app_get_tindakan_by_id(id: int, db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user),):
    return {"status": True, "message": "sukses", "data": get_tindakan_by_id(db=db, id=id)}
@app.post("/tindakan")
def app_create_tindakan(kondisi_awal: str = Form(...), tindakan: str = Form(...),
                kondisi_pasca: Optional[str] = Form(None), id_masalah: int = Form(...),
                id_ruangan: int = Form(...), id_sarana: int = Form(...),
                id_kategori: int = Form(...), foto: Optional[UploadFile] = File(None),
                current_user: user_schema.User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    response = None
    try:
        tindakan = TindakanCreate(kondisi_awal=kondisi_awal,tindakan=tindakan,
        kondisi_pasca=kondisi_pasca,id_user=current_user.id, id_masalah=id_masalah,
        id_sarana=id_sarana, id_kategori=id_kategori,
        id_ruangan=id_ruangan, foto=foto)
        response = create_tindakan(db=db,tindakan=tindakan)
        del tindakan
        return {"status": response[0], "message": response[1], "data": response[2]}
    except Exception as e: raise HTTPException(status_code = sts.HTTP_410_GONE,detail="Error = " + str(e))
    finally: del response
@app.put("/tindakan/{id}")
def app_create_tindakan(id: int, kondisi_awal: Optional[str] = Form(None), tindakan: Optional[str] = Form(None),
                kondisi_pasca: Optional[str] = Form(None), id_masalah: Optional[int] = Form(None),
                id_ruangan: Optional[int] = Form(None), id_sarana: Optional[int] = Form(None),
                id_kategori: Optional[int] = Form(None), foto: Optional[UploadFile] = File(None),
                current_user: user_schema.User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    response = None
    try:
        tindakan = TindakanUpdate(id=id,kondisi_awal=kondisi_awal,tindakan=tindakan,
        kondisi_pasca=kondisi_pasca,id_user=current_user.id, id_masalah=id_masalah,
        id_sarana=id_sarana, id_kategori=id_kategori,
        id_ruangan=id_ruangan, foto=foto)
        response = create_tindakan(db=db,tindakan=tindakan)
        del tindakan
        return {"status": response[0], "message": response[1], "data": response[2]}
    except Exception as e: raise HTTPException(status_code = sts.HTTP_410_GONE,detail="Error = " + str(e))
    finally: del response
@app.delete("/tindakan/{id}")
async def delete_tindakan_id(id: str, db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    response = None
    try:
        response = delete_tindakan_by_id(db=db, id=id)
        return {"status": response[0], "message": response[1], "data": response[2]}
    except Exception as e: return {"status": False, "message": "Error: " + str(e), "data": []}
    finally: del response
