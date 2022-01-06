from typing import Dict
from fastapi import HTTPException

from app.db.repositories.user import UserRepository
from app.db.repositories.data_type import DataTypeRepository
from app.models.user import UserInDB
from app.models.data_type import DataTypeInDB


async def check_user(user_repo: UserRepository, user_id: int) -> UserInDB:
    user = await user_repo.get_user(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def check_data_types(types_repo: DataTypeRepository, x_data_type: str, y_data_type: str) -> Dict[str, DataTypeInDB]:
    type_x = await types_repo.get_by_name(x_data_type)
    type_y = await types_repo.get_by_name(y_data_type)

    if type_x is None or type_y is None:
        raise HTTPException(status_code=404, detail="Wrong data types")

    types_dict = dict(
        x=type_x,
        y=type_y
    )

    return types_dict
