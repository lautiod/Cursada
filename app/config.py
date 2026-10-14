from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///datos/cursada.db"
    secret_key: str = "solo-para-desarrollo"


config = Config()
