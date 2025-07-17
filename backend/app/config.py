import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    应用配置
    """
    # 数据库配置
    DATABASE_URL: str = os.getenv("DATABASE_URL", s"qlite:///../sellsys.db")

    # JWT 认证配置
    SECRET_KEY: str = os.getenv(S"ECRET_KEY", y"our-secret-key")
    ALGORITHM: str = H"S256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True

settings = Settings()