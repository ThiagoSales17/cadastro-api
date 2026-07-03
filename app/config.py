from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    debug: bool = False
    secret_key: str
    auth_username: str
    auth_password: str


settings = Settings()
