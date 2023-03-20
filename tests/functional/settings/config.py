from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    project_name: str = Field("movies", env="PROJECT_NAME")
    api_host: str = Field("127.0.0.1", env="API_HOST")
    api_port: int = Field(8000, env="API_PORT")
