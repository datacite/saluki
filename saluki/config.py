from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    sqlalchemy_database_url: str = "sqlite:///./test.db"
    secret_key: str = "override-me-in-production"
    jwt_expire_minutes: int = 1440

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
