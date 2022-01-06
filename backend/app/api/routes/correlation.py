
from typing import Dict, Optional, Tuple

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_200_OK

from scipy.stats.stats import pearsonr

from app.models.correlation import CorrelationCreate, CorrelationPublic, UserCorrelation, CorrelationValue
from app.db.repositories.correlation import CorrelationRepository
from app.db.repositories.user import UserRepository
from app.db.repositories.data_type import DataTypeRepository
from app.db.repositories.user_data import UserDataRepository
from app.api.dependencies.database import get_repository  


from .common import check_user, check_data_types

router = APIRouter()


@router.get("/", response_model=CorrelationPublic, name="user:get-correlation", status_code=HTTP_200_OK)
async def get_correlation(
    x_data_type: str, y_data_type: str, user_id: int,
    correlation_repo: CorrelationRepository = Depends(get_repository(CorrelationRepository)),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    types_repo: DataTypeRepository = Depends(get_repository(DataTypeRepository)),
    user_data_repo: UserDataRepository = Depends(get_repository(UserDataRepository)),
) -> CorrelationPublic:
    user = await check_user(user_repo, user_id)
    types = await check_data_types(types_repo, x_data_type, y_data_type)

    user_corr = UserCorrelation(user_id=user_id, type_x_id=types['x'].id, type_y_id=types['y'].id)

    stored_corr = await correlation_repo.get_correlation(correlation=user_corr)

    if stored_corr is None or (user.last_data_change is not None and stored_corr.mtime < user.last_data_change):
        new_values = await calc_correlation(user_data_repo, user_id, types['x'].id, types['y'].id)

        if new_values is not None:
            new_corr = CorrelationCreate(user_id=user_id, type_x_id=types['x'].id, type_y_id=types['y'].id, correlation=new_values)
            stored_corr = await correlation_repo.upsert_correlation(new_correlation=new_corr)
    
    if stored_corr is None:
        raise HTTPException(status_code=404, detail="Correlation not found")
    else:
        result = CorrelationPublic(
            user_id=user_id,
            x_data_type=x_data_type,
            y_data_type=y_data_type,
            correlation=CorrelationValue(value=stored_corr.value, p_value=stored_corr.p_value)
            )

        return result


async def calc_correlation(user_data_repo, user_id: int, type_x_id: int, type_y_id: int) -> Optional[CorrelationValue]:
    user_data = dict()
    user_data['x'] = await user_data_repo.get_user_data_for_type(user_id, type_x_id)
    user_data['y'] = await user_data_repo.get_user_data_for_type(user_id, type_y_id)

    if not user_data['x'] or not user_data['y']:
        return

    data_by_dates = dict()

    for num, rows in user_data.items():
        for row in rows:
            tmp = dict(row)
            key = tmp['date'].isoformat()
            data_by_dates.setdefault(key, dict())
            data_by_dates[key][num] = tmp['value']
    
    data_to_process = dict(
        x=[],
        y=[]
    )

    for dt, values in data_by_dates.items():
        if len(values.keys()) != 2:
            continue
        for num, val in values.items():
            # @NOTICE: для разных типов данных тут можно проверять на 0 и отрицательность, например
            data_to_process[num].append(val)

    corr = calc_coeff(data_to_process['x'], data_to_process['y'])

    return corr


def calc_coeff(list1, list2) -> CorrelationValue:
    value, p_value = pearsonr(list1, list2)

    return CorrelationValue(value=value, p_value=p_value)
