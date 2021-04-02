from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime
from fastapi import UploadFile


class MasalahBase(BaseModel):
    _repr_hide = ['created_at', 'updated_at', 'deleted_at']
    deskripsi: Optional[str]

class MasalahCreate(MasalahBase):
    id_user: int
    id_kategori_masalah: int
    id_ruangan: int
    id_sarana: int
    foto: Optional[UploadFile]

class MasalahUpdate(MasalahBase):
    id: int
    id_level_1: Optional[int]
    id_level_2: Optional[int]
    id_level_3: Optional[int]
    id_kategori_masalah: Optional[int]
    id_ruangan: Optional[int]
    id_sarana: Optional[int]
    status: Optional[bool]
    foto: Optional[UploadFile]

class MasalahInfo(MasalahBase):
    id: Optional[int]
    id_user: Optional[int]
    id_kategori_masalah: Optional[int]
    id_ruangan: Optional[int]
    id_sarana: Optional[int]
    status: bool
    foto: Optional[str]

    class Config:
        orm_mode = True
