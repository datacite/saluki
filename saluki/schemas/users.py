from typing import Optional

from pydantic import BaseModel, EmailStr

from saluki.enums import UserLevel


# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    name: str


# Extra properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# Extra properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


# Extra properties stored in DB
class UserInDB(UserBase):
    id: int
    password: str
    user_level: UserLevel
    is_active: bool


# Extra properties to return via API
class User(UserBase):
    id: int
    user_level: UserLevel
    is_active: bool
