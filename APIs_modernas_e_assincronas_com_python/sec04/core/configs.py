from pydantic import BaseSettings, AnyHttpUrl
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    """Configurações gerais na aplicação"""
    API_V1_STR: str = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://geek:university@localhost:5432/faculdade"
    DBBaseModel = declarative_base()

    class Config:
        case_senitive = True


settings = Settings()
