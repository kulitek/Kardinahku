import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from typing import List, Optional, List, Any
from pydantic import BaseModel
from datetime import datetime


class InstalasiBase(BaseModel):
    _repr_hide = ['created_at', 'updated_at', 'deleted_at']
    nama: str

class Instalasi(InstalasiBase):
    id: int

class InstalasiRaw(BaseModel):
    data: List[Instalasi] = None

class InstalasiGetAll(BaseModel):
    status: Optional[bool] = True
    message: Optional[str] = "sukses"
    data: List[Instalasi] = None

# class InstalasiInfo(InstalasiBase):
#     id: int
#
#     ruangan: List[ruangan_schema.Ruangan] = []
#
#     class Config:
#         orm_mode = True
