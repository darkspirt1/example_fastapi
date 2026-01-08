from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from uvicorn import Config


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    phone_number: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: 'UserOut'
   

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone_number: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: int



class FileUploadOut(BaseModel):
    id: int
    filename: str
    uploaded_at: datetime
    owner : UserOut | None
   
    class Config:
        from_attributes = True
