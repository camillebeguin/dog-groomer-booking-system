from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: Optional[str]
    full_name: Optional[str]

class UserCreate(BaseModel):
    email: str 
    password: str 