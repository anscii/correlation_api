from typing import List
from app.db.repositories.base import BaseRepository
from app.models.user_data import UserDataCreate, UserDataUpdate, UserDataInDB, UserDataSaved


UPSERT_USER_DATA_QUERY = """
    INSERT INTO user_data (user_id, date, type_id, value)
    VALUES (:user_id, :date, :type_id, :value)
    ON CONFLICT ON CONSTRAINT user_data_unique
        DO UPDATE SET 
            value=EXCLUDED.value 
    RETURNING id, user_id, date, type_id, value;
"""

GEt_USER_DATA_QUERY = """
    SELECT id, user_id, date, type_id, value
    FROM user_data
    WHERE user_id = :user_id AND type_id = :type_id;
"""

class UserDataRepository(BaseRepository):
    """"
    All database actions associated with the UserData resource
    """

    async def get_user_data_for_type(self, user_id: int, type_id: int) -> List[UserDataInDB]:
        query_values = dict(user_id=user_id, type_id=type_id)
        user_data = await self.db.fetch_all(query=GEt_USER_DATA_QUERY, values=query_values)

        if user_data:
            result = [UserDataInDB(**row) for row in user_data]
            return result


    async def upsert_user_data(self, *, new_user_data: UserDataCreate, x_type_id: int, y_type_id: int) -> UserDataSaved:
        transaction = await self.db.transaction()
        count = 0

        try:
            for idx, type_data in enumerate((new_user_data.data.x, new_user_data.data.y)):
                for val in type_data:
                    values =  dict(
                            user_id=new_user_data.user_id,
                            date=val.date,
                            type_id=x_type_id if not idx else y_type_id,
                            value=val.value,
                            # mtime=datetime.now()
                        )

                await self.db.execute(query=UPSERT_USER_DATA_QUERY, values=values)
                count += 1

            # await set_user_last_data_change(db, user_data.user_id)  # @TODO: 
        except Exception as err:
            await transaction.rollback()
            raise err
        else:
            await transaction.commit()
        
        result = UserDataSaved(user_id=new_user_data.user_id, count=count)
        return result
