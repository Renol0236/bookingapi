from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserUpdate(BaseModel):
    username: str = None
    email: EmailStr = None


class Token(BaseModel):
    access_token: str
    token_type: str
