from uuid import UUID

from fastapi import APIRouter

from app.repository.groomer import GroomerRepository
from app.schema.groomer import GroomerBase

router = APIRouter()

@router.get('/groomer', response_model=list[GroomerBase])
def list_groomers(
    session, 
    page,
    per_page,
):
    return GroomerRepository.list_groomers(session, page=page, per_page=per_page)

@router.get('/groomer/{groomer_id}', response_model=GroomerBase)
def get_groomer(
    session, 
    groomer_id: UUID,
):
    return GroomerRepository.get(session, id=groomer_id)