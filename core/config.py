from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    # Base de Datos
    DATABASE_URL: str

    # Credenciales de Paideia (nombre idéntico al .env)
    URL_PAIDEIA: str
    MOODLE_WS_TOKEN: str

    # Seguridad JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 días

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Ignora variables sobrantes como DB_PASSWORD sin lanzar error
    )

settings = Config()