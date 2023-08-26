from sqlalchemy import Column, Integer, String

from app.model.base import BaseModel


class User(BaseModel):
    full_name = Column(String, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)