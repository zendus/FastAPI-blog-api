from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from .decorators import as_form

from pydantic.types import conint


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    is_active: bool

    class Config:
        orm_mode = True

class EmailSchema(BaseModel):
    email: List[EmailStr]


@as_form
class PostCreate(BaseModel):
    title: str
    content: str