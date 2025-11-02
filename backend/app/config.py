import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    psql_username: str = os.getenv("PSQL_USERNAME", "")
    psql_password: str = os.getenv("PSQL_PASSWORD", "")
    psql_database: str = os.getenv("PSQL_DATABASE", "")
    psql_port:     str = os.getenv("PSQL_PORT", "")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
