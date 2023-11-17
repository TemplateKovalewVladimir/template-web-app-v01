from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8")

    # to get a string like this run: openssl rand -hex 32
    SECRET_KEY: str = "418bf71df8aae0377dcc77e883d936900c2e465cdff3f52ae9aa59d5ef20bff0"
    JWT_ALGORITHM: str = "HS256"

    HOSTNAME: str = "no environ param $HOSTNAME"

    APP_NAME: str = "App"
    APP_TITLE: str = "App"

    # http://test1.ru,http://test2.ru
    HTTP_ALLOW_ORIGINS: str = ""

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

    # LDAP аутентификация
    LDAP_SERVER: str = ""
    LDAP_DOMAIN: str = ""

    # Для отправки почты
    MAIL_ENABLED: bool = False
    MAIL_HOST: str | None = None
    MAIL_USER: str | None = None
    MAIL_PASSWORD: str | None = None
    MAIL_FROM: str | None = None
    MAIL_TO: str | None = None
    MAIL_SUBJECT: str | None = None

    @property
    def get_http_allow_origins(self) -> list[str]:
        return self.HTTP_ALLOW_ORIGINS.split(",")

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
