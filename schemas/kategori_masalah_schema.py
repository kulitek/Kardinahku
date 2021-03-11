import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class KategoriMasalahBase(BaseModel):
    _repr_hide = ['created_at', 'updated_at', 'deleted_at']
    kategori: str

class KategoriMasalah(InstalasiBase):
    id: int

# class InstalasiInfo(InstalasiBase):
#     id: int
#
#     ruangan: List[ruangan_schema.Ruangan] = []
#
#     class Config:
#         orm_mode = True
