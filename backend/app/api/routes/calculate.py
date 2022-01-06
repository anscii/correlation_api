
from fastapi import APIRouter, Body, Depends  
from starlette.status import HTTP_200_OK

from app.models.user_data import UserDataCreate, UserDataSaved
from app.db.repositories.user_data import UserDataRepository
from app.db.repositories.user import UserRepository
from app.db.repositories.data_type import DataTypeRepository
from app.api.dependencies.database import get_repository  


from .common import check_user, check_data_types

router = APIRouter()


@router.post("/", response_model=UserDataSaved, name="user:store-data", status_code=HTTP_200_OK)
async def upload_user_data(
    user_data: UserDataCreate = Body(...),
    user_data_repo: UserDataRepository = Depends(get_repository(UserDataRepository)),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    types_repo: DataTypeRepository = Depends(get_repository(DataTypeRepository))
) -> UserDataSaved:
    await check_user(user_repo, user_data.user_id)
    types = await check_data_types(types_repo, user_data.data.x_data_type, user_data.data.y_data_type)

    stored_data = await user_data_repo.upsert_user_data(new_user_data=user_data, x_type_id=types['x'].id, y_type_id=types['y'].id)

    if stored_data is not None:
        await user_repo.refresh_last_data_change(user_data.user_id)

    return stored_data
