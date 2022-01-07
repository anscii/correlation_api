import urllib.parse

import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND


from app.models.correlation import CorrelationInput, CorrelationPublic
pytestmark = pytest.mark.asyncio

ROUTE_NAME = 'user:get-correlation'

@pytest.fixture
def user_correlation():
    return CorrelationInput(
        user_id=1,
        x_data_type='steps',
        y_data_type='avg_hr'
    )

class TestGetCorrelation:
    async def test_get_user_correlation(self, app: FastAPI, client: AsyncClient, user_correlation: CorrelationInput) -> None:
        url = app.url_path_for(ROUTE_NAME)
        params = urllib.parse.urlencode(user_correlation.dict())

        res = await client.get(f"{url}?{params}")

        assert res.status_code == HTTP_200_OK
        correlation = CorrelationPublic(**res.json())
        assert correlation.user_id == user_correlation.user_id
    
    @pytest.mark.parametrize(
        "user_id, x_data_type, y_data_type",
        (
            (666, 'steps', 'avg_hr'),
            (1, 'unknown???', 'avg_hr'),
        ),
    )
    async def test_wrong_params_return_error(
        self, app: FastAPI, client: AsyncClient, user_id: int, x_data_type: str, y_data_type: str
    ) -> None:
        user_correlation = CorrelationInput(
            user_id=user_id,
            x_data_type=x_data_type,
            y_data_type=y_data_type
        )
        url = app.url_path_for(ROUTE_NAME)
        params = urllib.parse.urlencode(user_correlation.dict())

        res = await client.get(f"{url}?{params}")

        assert res.status_code == HTTP_404_NOT_FOUND
