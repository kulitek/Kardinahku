from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from user_scheme import User


class PegawaiBase(BaseModel):
    __repr_hide = ['created_at', 'updated_at',]
    nama_lengkap: str
    tempat_lahir: Optional[str]
    jenis_kelamin: str
    tanggal_lahir: datetime

class PegawaiInfo(PegawaiBase):
    id: str

    user: Optional[User]

    class Config:
        orm_mode = True
