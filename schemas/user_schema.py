from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    _repr_hide = ['created_at', 'updated_at', 'deleted_at']
    username: Optional[str]

class UserRegister(UserBase):
    password: str
    email: str
    id_pegawai: int
    role: Optional[str]

class UserRegistered(UserBase):
    message: str

class UserLogin(UserBase):
    password: str

class UserUpdate(UserBase):
    id: int
    email: Optional[str]
    role: Optional[str]
    is_active: Optional[bool]

class User(UserBase):
    id: Optional[int]
    email: Optional[str]
    role: Optional[str]
    id_pegawai: Optional[str]
    token: Optional[str]

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None
