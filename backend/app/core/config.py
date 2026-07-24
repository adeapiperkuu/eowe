from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 14
    environment: str = "development"


settings = Settings()
