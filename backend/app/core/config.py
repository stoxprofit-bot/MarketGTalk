from functools import lru_cache

from cryptography.fernet import Fernet
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "CopyTrade API"
    api_v1_prefix: str = "/api/v1"
    secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "copytrade"
    coinswitch_base_url: str = "https://coinswitch.co"
    encryption_key: str
    tradingview_webhook_secret: str
    default_exchange: str = "c2c1"
    default_order_type: str = "limit"
    admin_emails: str = ""

    @computed_field
    @property
    def admin_email_list(self) -> list[str]:
        return [email.strip().lower() for email in self.admin_emails.split(",") if email.strip()]


@lru_cache
def get_fernet() -> Fernet:
    return Fernet(settings.encryption_key.encode())


settings = Settings()
