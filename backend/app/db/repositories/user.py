from typing import Optional
from app.db.repositories.base import BaseRepository
from app.models.user import UserCreate, UserUpdate, UserInDB


CREATE_USER_QUERY = """
    INSERT INTO public.user (name) VALUES (:name)
    RETURNING id, name, last_data_change;
"""

GET_USER_QUERY = """
    SELECT id, name, last_data_change
    FROM public.user
    WHERE id = :id
"""

UPDATE_USER_DATE_QUERY = """
    UPDATE public.user
    SET last_data_change = NOW()
    WHERE id = :id
"""

class UserRepository(BaseRepository):
    """"
    All database actions associated with the User resource
    """
    async def create_user(self, *, new_user: UserCreate) -> UserInDB:
        query_values = new_user.dict()
        user = await self.db.fetch_one(query=CREATE_USER_QUERY, values=query_values)
        return UserInDB(**user)

    async def get_user(self, user_id: int) -> Optional[UserInDB]:
        query_values = dict(id=user_id)
        user = await self.db.fetch_one(query=GET_USER_QUERY, values=query_values)

        if user:
            return UserInDB(**user)
    
    async def refresh_last_data_change(self, user_id: int) -> None:
        query_values = dict(id=user_id)
        await self.db.fetch_one(query=UPDATE_USER_DATE_QUERY, values=query_values)
