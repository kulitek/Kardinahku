from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime



class UserInfoBase(BaseModel):
    _repr_hide = ['created_at', 'updated_at']
    username: str


class UserCreate(UserInfoBase):
    username: str
    password: str
    fullname: Optional[str] = None
    email: Optional[str] = None


class UserAuthenticate(UserInfoBase):
    password: str

class UserUpdate(BaseModel):
    id: int
    fullname: Optional[str]
    email: Optional[str]
    is_active: Optional[bool]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class ItemBase(BaseModel):
    title: str
    content: str
    owner_id: int


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserInfo(UserInfoBase):
    id: int
    fullname: Optional[str]
    email: Optional[str]
    is_active: Optional[bool]

    items: List[Item] = []

    class Config:
        orm_mode = True

class UserUpdated(UserInfo):
    pass

class UserDeleted(UserInfo):
    deleted_at: Optional[datetime]

class ItemUpdated(Item):
    pass

class ItemDeleted(Item):
    deleted_at: Optional[datetime]
