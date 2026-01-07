from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_name: str = ""
    db_pwd: str = ""
    db_user: str = ""
    db_port: int = 5432

    debug = False
    host: str = "0.0.0.0"
    ports: int = 8080
    workers: int = 4

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
