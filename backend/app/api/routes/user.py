
from fastapi import APIRouter, Body, Depends  
from starlette.status import HTTP_201_CREATED  

from app.models.user import UserCreate, UserPublic
from app.db.repositories.user import UserRepository
from app.api.dependencies.database import get_repository  

router = APIRouter()


@router.post("/", response_model=UserPublic, name="user:create-user", status_code=HTTP_201_CREATED)
async def create_new_user(
    new_user: UserCreate = Body(..., embed=True),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> UserPublic:
    created_user = await user_repo.create_user(new_user=new_user)
    return created_user
