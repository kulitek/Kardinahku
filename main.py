import uvicorn
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, logger
from starlette import status
from typing import List, Any, Iterator
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.ext.sqlalchemy import paginate

import models, schemas, crud
from app_utils import decode_access_token
from crud import get_user_by_username
from database import engine, SessionLocal
from schemas import UserInfo, TokenData
from enum import Enum


models.Base.metadata.create_all(bind=engine)


ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Dependency

def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authenticate")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(data=token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

class RoleChecker():
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User: Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            logger.debug(f"User with role {user.role} not in {self.allowed_roles}")
            raise HTTPException(status_code=403, detail="Operation not permitted.")

# @app.get("/users/page")
# def get_user_pagination(page: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return crud.get_users_pagination(db, page, limit)

@app.get("/users/", response_model=Page[schemas.UserInfo], dependencies=[Depends(pagination_params)])
def read_users(db: Session = Depends(get_db)) -> Any:
    # return crud.get_users(db)
    return paginate(crud.get_users(db))

@app.get("/users/{id}", response_model=schemas.UserInfo)
def get_user_id(db: Session = Depends(get_db), id: int = None) -> Any:
    return crud.get_user_by_id(db=db, id=id)

@app.post("/users", response_model=schemas.UserInfo)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.put("/users/", response_model=schemas.UserUpdated)
def update_user(user: schemas.UserUpdate, db: Session=Depends(get_db)) -> Any:
    if id is None:
        raise HTTPException(status_code=400, detail="Id must be included in parameter")
    return crud.update_user(db=db, user=user)

@app.delete("/users/{id}", response_model=schemas.UserDeleted)
def delete_user(db: Session=Depends(get_db), id: int = None):
    if id is None:
        raise HTTPException(status_code=400, detail="Id must be included in parameter")
    return crud.delete_user(db=db, id=id)


@app.post("/authenticate", response_model=schemas.Token)
def authenticate_user(user: schemas.UserAuthenticate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Username not existed")
    else:
        is_password_correct = crud.check_username_password(db, user)
        if is_password_correct is False:
            raise HTTPException(status_code=400, detail="Password is not correct")
        else:
            from datetime import timedelta
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            from app_utils import create_access_token
            access_token = create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "Bearer"}


@app.post("/items", response_model=schemas.Item)
async def create_new_blog(item: schemas.ItemBase, current_user: UserInfo = Depends(get_current_user), db: Session = Depends(get_db)):
    item.owner_id = current_user.id
    return crud.create_new_item(db=db, item=item)

#
@app.get("/items", response_model=Page[schemas.Item], dependencies=[Depends(pagination_params)])
async def get_all_items(current_user: UserInfo = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_all_items(db=db)


@app.get("/items/{id}", response_model=schemas.Item)
async def get_all_items(id: int, current_user: UserInfo = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_item_by_id(db=db, item_id=id)
#
# @app.get("/blog/{blog_id}")
# async def get_blog_by_id(blog_id, current_user: UserInfo = Depends(get_current_user), db: Session = Depends(get_db)):
#     return crud.get_blog_by_id(db=db, blog_id=blog_id)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8081)
