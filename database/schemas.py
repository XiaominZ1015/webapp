from typing import List, Union, Optional

from pydantic import BaseModel

# Pydantic models
# use EmailStr for email type
class UserBase(BaseModel):
    first_name: str
    last_name: str

class UserCreate(UserBase):
    username: str
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]
    verify: Optional[int]

class User(UserBase):
    id: int
    username: str
    accountCreated: str
    accountupdated: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class DocData(BaseModel):
    doc_id: str
    user_id: str
    name: str
    data_created: str
    s3_bucket_path: str

class DocMetaData(BaseModel):
    doc_id: str
    user_id: str
    name: str
    s3_bucket_path: str