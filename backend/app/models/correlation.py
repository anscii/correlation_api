from datetime import datetime, date
from app.models.core import IDModelMixin, CoreModel


class CorrelationBase(CoreModel):
    """
    All common characteristics of our Correlation
    """
    user_id: int

class CorrelationValue(CoreModel):
    value: float
    p_value: float

class CorrelationCreate(CorrelationBase):
    type_x_id: int
    type_y_id: int
    correlation: CorrelationValue

class UserCorrelation(CorrelationBase):
    type_x_id: int
    type_y_id: int

class CorrelationInDB(IDModelMixin, CorrelationBase):
    user_id: int
    type_x_id: int
    type_y_id: int
    value: float
    p_value: float
    mtime: datetime

class CorrelationPublic(CorrelationBase):
    x_data_type: str
    y_data_type: str
    correlation: CorrelationValue

class CorrelationInput(CorrelationBase):
    x_data_type: str
    y_data_type: str