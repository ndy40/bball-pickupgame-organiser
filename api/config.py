from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_FILE: str

    SECRET: str = "!changeme!"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
