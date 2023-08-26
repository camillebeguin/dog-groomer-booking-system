from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from app.model.base import BaseModel


class Reservation(BaseModel):
    groomer_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time: Column(DateTime, nullable=False)
    pet_type: Column(String, nullable=False)