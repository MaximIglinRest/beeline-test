from fastapi import FastAPI

from core.config import settings

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)
