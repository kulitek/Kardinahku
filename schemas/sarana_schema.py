import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi import Form, UploadFile


# def form_body_required(cls):
#     cls.__signature__ = cls.__signature__.replace(
#         parameters=[
#             arg.replace(default=Form(...))
#             for arg in cls.__signature__.parameters.values()
#         ]
#     )
#     return cls
#
# def form_body(cls):
#     cls.__signature__ = cls.__signature__.replace(
#         parameters=[
#             arg.replace(default=Form(None))
#             for arg in cls.__signature__.parameters.values()
#         ]
#     )
#     return cls


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

class SaranaUpdate(BaseModel):
    id: int
    nama: Optional[str] = None
    id_ruangan: Optional[int] = None
    id_jenis: Optional[int] = None
    foto: Optional[UploadFile] = None
    berat: Optional[str] = None
    panjang: Optional[str] = None
    tinggi: Optional[str] = None
    lebar: Optional[str] = None

# @form_body
# class SaranaUpdateForm(BaseModel):
#     id: int
#     nama: Optional[str] = None
#     id_ruangan: Optional[int] = None
#     id_jenis: Optional[int] = None
#     foto: Optional[UploadFile] = None
#     berat: Optional[str] = None
#     panjang: Optional[str] = None
#     tinggi: Optional[str] = None
#     lebar: Optional[str] = None



# class InstalasiInfo(InstalasiBase):
#     id: int
#
#     ruangan: List[ruangan_schema.Ruangan] = []
#
#     class Config:
#         orm_mode = True
