import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi import Form, UploadFile



class SaranaBase(BaseModel):
    _repr_hide = ['created_at', 'updated_at', 'deleted_at']
    nama: str

class Sarana(SaranaBase):
    id: int

class SaranaCreate(BaseModel):
    nama: str
    id_ruangan: int
    id_jenis: int
    foto: UploadFile

class SaranaCreate(BaseModel):
    id: int
    nama: Optional[str] = None
    id_ruangan: Optional[int] = None
    id_jenis: Optional[int] = None
    foto: Optional[UploadFile] = None



# class InstalasiInfo(InstalasiBase):
#     id: int
#
#     ruangan: List[ruangan_schema.Ruangan] = []
#
#     class Config:
#         orm_mode = True
