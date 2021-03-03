from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class PegawaiBase(BaseModel):
    __repr_hide = ['created_at', 'updated_at',]
    
