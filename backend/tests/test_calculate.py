import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from fastapi.encoders import jsonable_encoder

from app.models.user_data import UserDataCreate, DataInput, DateValue, UserDataSaved

pytestmark = pytest.mark.asyncio

ROUTE_NAME = 'user:store-data'

@pytest.fixture
def new_user_data():
    x_values = []
    y_values = []

    x_values.append(DateValue(date='2022-01-07', value=5555))
    y_values.append(DateValue(date='2022-01-07', value=78.13))

    data = DataInput(
        x_data_type='steps',
        y_data_type='avg_hr',
        x=x_values,
        y=y_values
    )
    return UserDataCreate(
        user_id=1,
        data=data
    )

class TestCalculateRoutes:

    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for(ROUTE_NAME), json={})
        assert res.status_code != HTTP_404_NOT_FOUND

    async def test_invalid_input_raises_error(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for(ROUTE_NAME), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY


class TestStoreUserData:
    async def test_valid_input_user_data(
        self, app: FastAPI, client: AsyncClient, new_user_data: UserDataCreate
    ) -> None:
        res = await client.post(
            app.url_path_for(ROUTE_NAME), json=jsonable_encoder(new_user_data)
        )
        assert res.status_code == HTTP_200_OK

        saved_user_data = UserDataSaved(**res.json())
        assert saved_user_data.user_id == new_user_data.user_id
        assert saved_user_data.count == len(new_user_data.data.x) + len(new_user_data.data.y)

    async def test_invalid_user(
        self, app: FastAPI, client: AsyncClient, new_user_data: UserDataCreate
    ) -> None:
        new_user_data.user_id = 999

        res = await client.post(
            app.url_path_for(ROUTE_NAME), json=jsonable_encoder(new_user_data)
        )
        assert res.status_code == HTTP_404_NOT_FOUND

    async def test_invalid_data_type(
        self, app: FastAPI, client: AsyncClient, new_user_data: UserDataCreate
    ) -> None:
        new_user_data.data.x_data_type = 'unknown_type'

        res = await client.post(
            app.url_path_for(ROUTE_NAME), json=jsonable_encoder(new_user_data)
        )
        assert res.status_code == HTTP_404_NOT_FOUND
