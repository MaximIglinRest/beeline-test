from fastapi import FastAPI

from api.v1.auth import user
from core.config import settings

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)

app.include_router(user.router, prefix="/api/v1/user", tags=["auth"])
