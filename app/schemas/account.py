from pydantic import BaseModel, EmailStr
from typing import Optional

class AccountRequest(BaseModel):
    image: str
    username: str
    password: str
    email: EmailStr
    phone: str

class AccountResponse(BaseModel):
    id: Optional[int] = None
    image: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

    class Config:
        orm_mode = True