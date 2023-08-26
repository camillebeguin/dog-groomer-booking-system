from sqlalchemy import Column, Integer, String

from app.model.base import BaseModel


class Groomer(BaseModel):
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    description = Column(String, nullable=True)
    address = Column(String, nullable=False)
