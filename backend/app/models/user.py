from datetime import datetime
from typing import Optional
from app.models.core import IDModelMixin, CoreModel


class UserBase(CoreModel):
    """
    All common characteristics of our User
    """
    name: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    # last_data_change: datetime
    pass

class UserInDB(IDModelMixin, UserBase):
    last_data_change: Optional[datetime]

class UserPublic(IDModelMixin, UserBase):
    pass
