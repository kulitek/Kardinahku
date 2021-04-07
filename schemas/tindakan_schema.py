from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime
from fastapi import UploadFile


class TindakanBase(BaseModel):
    _repr_hide = ['created_at', 'updated_at', 'deleted_at']
    kondisi_awal: Optional[str]
    tindakan: Optional[str]
    kondisi_pasca: Optional[str]

class TindakanCreate(TindakanBase):
    id_user: int
    id_masalah: int
    id_kategori: int
    id_ruangan: int
    id_sarana: int
    foto: Optional[UploadFile]

class TindakanUpdate(TindakanBase):
    id: int
    id_user: Optional[int]
    id_masalah: Optional[int]
    id_kategori: Optional[int]
    id_ruangan: Optional[int]
    id_sarana: Optional[int]
    foto: Optional[UploadFile]

class TindakanInfo(TindakanBase):
    id: Optional[int]
    id_user: Optional[int]
    id_kategori_masalah: Optional[int]
    id_ruangan: Optional[int]
    id_sarana: Optional[int]
    status: bool
    foto: Optional[str]

    class Config:
        orm_mode = True
