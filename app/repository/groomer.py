from typing import Optional

from app import model
from app.core.enums import PetType

from .base import BaseRepository


class _GroomerRepository(BaseRepository):
    def list_groomers(self, session, page: int = 1, per_page: int = 10):
        filters = []

        query = (
            self.query(session=session)
            .filter(*filters)
            .order_by(self.model.created_at.desc())
        )

        return self.as_paginated_query(query, page=page, per_page=per_page)

GroomerRepository = _GroomerRepository(model=model.Groomer)