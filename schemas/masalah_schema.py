from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime


class MasalahBase(BaseModel):
    _repr_hide = ['created_at', 'updated_at', 'deleted_at']
    deskripsi: Optional[str]

class MasalahRegister(MasalahBase):
    password: str
    email: str
    id_pegawai: int
    role: Optional[str]

class MasalahRegistered(MasalahBase):
    api_token: str

class MasalahLogin(MasalahBase):
    password: str

class MasalahUpdate(MasalahBase):
    id: int
    email: Optional[str]
    role: Optional[str]
    is_active: Optional[bool]

class Masalah(MasalahBase):
    id: Optional[int]
    email: Optional[str]
    role: Optional[str]
    id_pegawai: Optional[str]
    token: Optional[str]

    class Config:
        orm_mode = True

class Token(BaseModel):
    status: bool
    message: str
    data: MasalahRegistered

class TokenData(BaseModel):
    username: str = None
