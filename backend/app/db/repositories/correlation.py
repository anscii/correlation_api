from app.db.repositories.base import BaseRepository
from app.models.correlation import CorrelationCreate, CorrelationInDB, UserCorrelation

UPSERT_CORRELATION_QUERY = """
    INSERT INTO correlation (user_id, type_x_id, type_y_id, value, p_value)
    VALUES (:user_id, :type_x_id, :type_y_id, :value, :p_value)
    ON CONFLICT ON CONSTRAINT correlation_unique
        DO UPDATE SET 
            value=EXCLUDED.value, 
            p_value=EXCLUDED.p_value,
            mtime=EXCLUDED.mtime
    RETURNING id, user_id, type_x_id, type_y_id, value, p_value, mtime;
"""

GET_CORRELATION_QUERY = """
    SELECT id, user_id, type_x_id, type_y_id, value, p_value, mtime
    FROM correlation
    WHERE user_id = :user_id AND (
        (type_x_id = :type_x_id AND type_y_id = :type_y_id)
        OR (type_x_id = :type_y_id AND type_y_id = :type_x_id)
        );
"""

class CorrelationRepository(BaseRepository):
    """"
    All database actions associated with the Correlation resource
    """
    async def upsert_correlation(self, *, new_correlation: CorrelationCreate) -> CorrelationInDB:
        query_values = dict(
            user_id=new_correlation.user_id,
            type_x_id=new_correlation.type_x_id,
            type_y_id=new_correlation.type_y_id,
            value=new_correlation.correlation.value,
            p_value=new_correlation.correlation.p_value
        )
        correlation = await self.db.fetch_one(query=UPSERT_CORRELATION_QUERY, values=query_values)

        return CorrelationInDB(**correlation)

    async def get_correlation(self, *, correlation: UserCorrelation) -> CorrelationInDB:
        query_values = correlation.dict()
        correlation = await self.db.fetch_one(query=GET_CORRELATION_QUERY, values=query_values)

        if correlation:
            return CorrelationInDB(**correlation)
