from app import model

from .base import BaseRepository


class _ReservationRepository(BaseRepository):
    ...

ReservationRepository = _ReservationRepository(model=model.Reservation)