import uvicorn
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, logger
from starlette import status
from typing import List, Any, Iterator
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.ext.sqlalchemy import paginate

import models
from controllers.user_controller import *
import schemas.user_scheme as schema
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

@app.post("/login", response_model=schema.Token)
def login_user(user: schema.UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db=db, username=user.username)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Username tidak ditemukan.")
    else:
        is_password_correct = check_username_password(db, user)
        if is_password_correct is False:
            raise HTTPException(status_code=400, detail="Password salah.")
        else:
            access_token = create_permanent_access_token(data={"sub": user.username})
            return {"access_token": access_token, "token_type": "normal"}

@app.post("/register", response_model=schema.User)
def registering_user(user: schema.UserRegister, db: Session=Depends(get_db)):
    db_user = get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username sudah terpakai.")
    else:
        return create_user(db=db, user=user)
