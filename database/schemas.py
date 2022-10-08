from typing import List, Union, Optional

from pydantic import BaseModel

# Pydantic models
# use EmailStr for email type
class UserBase(BaseModel):
    first_name: str
    last_name: str

class UserCreate(UserBase):
    email: str
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]

class User(UserBase):
    id: int
    email: str
    accountCreated: str
    accountupdated: str

class Token(BaseModel):
    access_token: str
    token_type: str