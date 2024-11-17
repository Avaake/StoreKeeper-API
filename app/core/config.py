from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn
from dotenv import load_dotenv

load_dotenv()


class APIPrefixes(BaseModel):
    api_v1_prefix: str = "/api/v1"
    user_auth: str = "/user/auth"


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class JWTConfig(BaseModel):
    secret_key: str = "super_secret_key"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    testing: bool = False
    db: DatabaseConfig
    jwt: JWTConfig = JWTConfig()
    api_prefix: APIPrefixes = APIPrefixes()


class TestingSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env_test",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    testing: bool = True
    db: DatabaseConfig
    jwt: JWTConfig = JWTConfig()
    api_prefix: APIPrefixes = APIPrefixes()


settings = Settings()
test_settings = TestingSettings()
