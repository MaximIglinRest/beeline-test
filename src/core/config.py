from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    JWT_SECRET = Field("some_secret", env="SECRET")
    JWT_ALGORITHM = Field("HS256", env="HASH_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_TIME = 600

    postgres_host: str = Field("127.0.0.1", env="POSTGRES_HOST")
    postgres_port: int = Field(5432, env="POSTGRES_PORT")
    db_name: str = Field("users_db", env="POSTGRES_DB")
    db_user: str = Field(env="POSTGRES_USER")
    db_password: str = Field(env="POSTGRES_PASSWORD")

    project_name = "BeelineTest"
    docs_url = ("/api/openapi",)
    openapi_url = "/api/openapi.json"


settings = Settings()
