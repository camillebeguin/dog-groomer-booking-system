from app import model

from .base import BaseRepository


class _UserRepository(BaseRepository):
    ...

UserRepository = _UserRepository(model=model.User)
