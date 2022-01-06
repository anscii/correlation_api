from typing import Optional
from app.db.repositories.base import BaseRepository
from app.models.data_type import DataTypeCreate, DataTypeUpdate, DataTypeInDB


CREATE_DATA_TYPE_QUERY = """
    INSERT INTO data_type (name) VALUES (:name)
    RETURNING id, name;
"""

GET_BY_NAME_QUERY = """
    SELECT id, name
    FROM data_type
    WHERE name = :name;
"""

class DataTypeRepository(BaseRepository):
    """"
    All database actions associated with the DataType resource
    """
    async def create_data_type(self, *, new_data_type: DataTypeCreate) -> DataTypeInDB:
        query_values = new_data_type.dict()
        data_type = await self.db.fetch_one(query=CREATE_DATA_TYPE_QUERY, values=query_values)
        return DataTypeInDB(**data_type)

    async def get_by_name(self, name: str) -> Optional[DataTypeInDB]:
        query_values = dict(name=name)
        data_type = await self.db.fetch_one(query=GET_BY_NAME_QUERY, values=query_values)

        if data_type:
            return DataTypeInDB(**data_type)
