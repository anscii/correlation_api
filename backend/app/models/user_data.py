from datetime import datetime, date
from typing import List
from app.models.core import IDModelMixin, CoreModel


class UserDataBase(CoreModel):
    """
    All common characteristics of our UserData
    """
    user_id: int

class DateValue(CoreModel):
    date: date
    value: float


class DataInput(CoreModel):
    x_data_type: str
    y_data_type: str
    x: List[DateValue]
    y: List[DateValue]

class UserDataCreate(UserDataBase):
    data: DataInput

class UserDataUpdate(UserDataBase):
    value: float
    # mtime: datetime

class UserDataInDB(IDModelMixin, UserDataBase):
    user_id: int
    date: date
    type_id: int
    value: float
    # mtime: datetime

class UserDataPublic(IDModelMixin, UserDataBase):
    count: int

class UserDataSaved(UserDataBase):
    user_id: int
    count: int