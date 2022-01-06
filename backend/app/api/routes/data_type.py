
from fastapi import APIRouter, Body, Depends  
from starlette.status import HTTP_201_CREATED  

from app.models.data_type import DataTypeCreate, DataTypePublic  
from app.db.repositories.data_type import DataTypeRepository
from app.api.dependencies.database import get_repository

router = APIRouter()

@router.post("/", response_model=DataTypePublic, name="datatype:create-data-type", status_code=HTTP_201_CREATED)
async def create_new_data_type(
    new_data_type: DataTypeCreate = Body(..., embed=True),
    data_type_repo: DataTypeRepository = Depends(get_repository(DataTypeRepository)),
) -> DataTypePublic:
    created_data_type = await data_type_repo.create_data_type(new_data_type=new_data_type)
    return created_data_type
