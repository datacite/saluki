from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    sqlalchemy_database_url: str = "sqlite:///./test.db"
    secret_key: str = "override-me-in-production"
    jwt_expire_minutes: int = 1440
    mailgun_api_key: str = "override-me-in-production"
    mailgun_domain: str = "mg.datacite.org"
    mailgun_endpoint: str = "https://api.mailgun.net/v3/mg.datacite.org"
    email_from: str = "DataCite Data Files Service"
    email_address: str = "support@datacite.org"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
