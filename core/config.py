from pydantic_settings import BaseSettings, SettingsConfigDict


class PaymentConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    def get_credentials(self, service: str) -> dict:
        prefix = f"{service.upper()}_"
        return {
            key.removeprefix(prefix).lower(): getattr(self, key)
            for key in self.model_fields
            if key.startswith(prefix)
        }
