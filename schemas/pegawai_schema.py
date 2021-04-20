from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from .user_schema import *


class PegawaiBase(BaseModel):
    __repr_hide = ['created_at', 'update_at', 'deleted_at']
    nama_lengkap: Optional[str]
    tempat_lahir: Optional[str]
    jenis_kelamin: Optional[str]
    tanggal_lahir: Optional[datetime]
    no_hp: Optional[str]
    no_wa: Optional[str]

class PegawaiInfo(PegawaiBase):
    id: Optional[int]
    nama_panggilan: Optional[str]

class Pegawai(PegawaiBase):
    id: str

    user: Optional[User]

    class Config:
        orm_mode = True
