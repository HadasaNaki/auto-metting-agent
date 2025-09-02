import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Database
    postgres_db: str = "smartagent"
    postgres_user: str = "smart"
    postgres_password: str = "agent"
    postgres_host: str = "db"
    postgres_port: int = 5432

    # Redis
    redis_host: str = "redis"
    redis_port: int = 6379

    # Object Storage
    minio_endpoint: str = "minio:9000"
    minio_access_key: str = "minio"
    minio_secret_key: str = "minio123"

    # Auth
    jwt_secret: str = "supersecret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # External APIs
    openai_api_key: str = ""
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/0"

    class Config:
        env_file = ".env"


settings = Settings()
