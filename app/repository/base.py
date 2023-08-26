from fastapi.encoders import jsonable_encoder


class BaseRepository:
    def __init__(self, model):
        self.model = model

    def _query(self, session, *_, **kwargs):
        filters = [getattr(self.model, k) == v for k, v in kwargs.items()]
        return session.query(self.model).filter(*filters)
    
    def get(self, session, *_, **kwargs):
        return self._query(session, **kwargs).one_or_none()
    
    def get_many(self, session, *_, **kwargs):
        return self._query(session, **kwargs).all()
    
    @staticmethod 
    def save(session, item, refresh=True):
        items = item if isinstance(item, list) else [item]
        session.add_all(items)
        session.commit()

        if refresh:
            for each in items:
                session.refresh(each)

        return item
    
    def create(self, session, obj_in, *args, **kwargs):
        db_obj = self.model(**jsonable_encoder(obj_in))
        session.add(db_obj)
        return self.save(session, db_obj)
    
    def update(self, session, db_obj, obj_in):
        update_data = (
            obj_in if isinstance(obj_in, dict) 
            else obj_in.dict(exclude_unset=True, exclude={"id"})
        )

        for field in update_data:
            setattr(db_obj, field, update_data[field])

        return self.save(session, db_obj)
    
    @staticmethod 
    def delete(session, obj_in):
        session.delete(obj_in)
        session.commit()
        return True 
    
    @staticmethod
    def as_paginated_query(query, page: int, per_page: int) -> tuple[int, list]:
        return query.count(), query.limit(per_page).offset((page - 1) * per_page).all()
