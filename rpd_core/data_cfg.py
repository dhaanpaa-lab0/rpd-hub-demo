from os import environ
from urllib.parse import quote


class DataConfig:

    @property
    def pg_db(self):
        return environ.get("PG_DB", "rpd")

    @property
    def pg_host(self):
        return environ.get("PG_HOST", "localhost")

    @property
    def pg_port(self):
        return environ.get("PG_PORT", "5432")

    @property
    def pg_user(self):
        return environ.get("PG_USER", environ.get("USER"))

    @property
    def pg_password(self):
        return quote(environ.get("PG_PASS", "***"))

    @property
    def pg_url_sqlalchemy(self):
        return f"postgresql+psycopg://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_db}"

    @property
    def pg_url(self):
        return f"postgresql://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_db}"
