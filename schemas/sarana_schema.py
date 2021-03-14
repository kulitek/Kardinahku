import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi import Form


class SaranaBase(BaseModel):
    _repr_hide = ['created_at', 'updated_at', 'deleted_at']
    nama: str

class Sarana(InstalasiBase):
    id: int

class SaranaCreate(BaseModel):
    nama: str = Form(...)
    


# class InstalasiInfo(InstalasiBase):
#     id: int
#
#     ruangan: List[ruangan_schema.Ruangan] = []
#
#     class Config:
#         orm_mode = True
