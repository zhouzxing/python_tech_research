from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv("ENVIRONMENT",'dev')}",           # 指定 .env 文件
        env_file_encoding="utf-8",
        case_sensitive=False,      # 大小写不敏感 <-
        extra="ignore",            # 忽略 .env 中多余的键
    )

    database_url: str
    debug: bool = False
    secret_key: str
    log_level: str = "INFO"


settings = Settings()

print(settings.model_config)
print(settings.database_url)
print(settings.debug)
print(settings.secret_key)
print(settings.log_level)