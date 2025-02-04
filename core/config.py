from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()
class PaymentConfig(BaseSettings):
    """
    Config Class to get the environment variables from the .env file.
    We can mention env variables and fetch them dynamically which will somewhat reduce the
    redundancy and make it simpler to access those variables.
    """
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    def get_credentials(self, service: str) -> dict:
        """
        Function that basically fetches the credentials which matches the prefix sent from the function with the
        variables, and then returns the credentials by removing the prefix.
        """
        prefix = f"{service.upper()}_"
        credentials = {}
        for key, value in os.environ.items():
            if key.startswith(prefix):
                # Remove prefix and convert the remaining part to lowercase
                credentials[key[len(prefix):].lower()] = value
        return credentials
