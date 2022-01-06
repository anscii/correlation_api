from app.models.core import IDModelMixin, CoreModel


class DataTypeBase(CoreModel):
    """
    All common characteristics of our DataType
    """
    name: str

class DataTypeCreate(DataTypeBase):
    name: str

class DataTypeUpdate(DataTypeBase):
    name: str

class DataTypeInDB(IDModelMixin, DataTypeBase):
    name: str

class DataTypePublic(IDModelMixin, DataTypeBase):
    pass
