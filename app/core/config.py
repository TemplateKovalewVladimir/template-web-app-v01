from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8")

    HOSTNAME: str = "no environ param $HOSTNAME"

    APP_NAME: str = "App"
    APP_TITLE: str = "App"

    # Для базы данных
    DB_HOST: str = ""
    DB_PORT: int = 5432
    DB_USER: str = ""
    DB_PASS: str = ""
    DB_NAME: str = ""

    # Логи
    LOG_FOLDER: str = "/var/log/"

    # SSO аутентификация (Kerberos)
    SSO_SPN: str = ""

    # Для отправки почты
    MAIL_ENABLED: bool = False
    MAIL_HOST: str | None = None
    MAIL_USER: str | None = None
    MAIL_PASSWORD: str | None = None
    MAIL_FROM: str | None = None
    MAIL_TO: str | None = None
    MAIL_SUBJECT: str | None = None

    @property
    def get_log_folder(self) -> str:
        return self.LOG_FOLDER + self.APP_NAME.lower()

    @property
    def database_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def database_url_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def database_url_psycopg3(self):
        return (
            f"host={self.DB_HOST} "
            f"port={self.DB_PORT} "
            f"dbname={self.DB_NAME} "
            f"user={self.DB_USER} "
            f"password={self.DB_PASS}"
        )


settings = Settings()
