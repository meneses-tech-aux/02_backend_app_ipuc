from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Credenciales de Paideia
    URL_PAIDEIA: str
    WS_TOKEN: str

    # Seguridad JWT
    SECRET_KEY: str = "V1Ohmzi4nuVChtDA"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200 # 30 DIAS

settings = Config()

