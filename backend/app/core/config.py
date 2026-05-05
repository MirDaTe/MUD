
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "낙화검심"
    SECRET_KEY: str = "change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    DATABASE_URL: str = "sqlite:///./data/nakhwa.db"
    WS_HEARTBEAT: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
