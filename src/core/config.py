from pydantic import BaseSettings


class Settings(BaseSettings):
    project_name = "BeelineTest"
    docs_url = ("/api/openapi",)
    openapi_url = "/api/openapi.json"


settings = Settings()
