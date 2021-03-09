import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import schemas.instalasi_schema as instalasi_schema


class RuangBase(BaseModel):
    _repr_hide = ['created_at', 'updated_at', 'deleted_at']
    nama: Optional[str]

class RuanganCreate(RuangBase):
    id_instalasi: int

class Ruangan(RuangBase):
    id: Optional[int]

class RuanganInfo(RuangBase):
    id: Optional[int]
    id_instalasi: Optional[int]

    instalasi: Optional[instalasi_schema.Instalasi] = None

    class Config:
        orm_mode = True
