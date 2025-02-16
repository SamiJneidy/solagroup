from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    db_hostname: str
    db_name: str
    db_port: int
    db_username: str
    db_password: str
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()