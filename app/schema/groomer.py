from pydantic import BaseModel


class GroomerBase(BaseModel):
    name: str
    price: int 
    status: str
    description: str | None 
    address: str
