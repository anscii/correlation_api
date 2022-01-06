from typing import Optional, Dict
from fastapi import FastAPI, HTTPException

from app.api.routes import router as api_router
from app.core import config, common


def get_app():
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    app.add_event_handler("startup", common.create_start_app_handler(app))
    app.add_event_handler("shutdown", common.create_stop_app_handler(app))

    app.include_router(api_router)

    return app

app = get_app()
