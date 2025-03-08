import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = os.environ.get('SECRET_KEY')
    GATEWAY_TIMEOUT: int = 59

    # URLs for the microservices.
    USERS_SERVICE_URL: str = os.environ.get('USERS_SERVICE_URL')

settings = Settings()
