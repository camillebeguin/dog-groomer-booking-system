import re
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative

table_name_pattern = re.compile(r"(?<!^)(?=[A-Z])")

class CustomUUID(postgresql.UUID):
    python_type = uuid.UUID

@as_declarative()
class BaseModel:
    id = Column(CustomUUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(DateTime(), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        DateTime(),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=datetime.utcnow,
    )

    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return re.sub(table_name_pattern, r"_", cls.__name__).lower()
