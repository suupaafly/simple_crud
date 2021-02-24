import pydantic


class Settings(pydantic.BaseSettings):
    db_uri = 'postgresql://user:pass@localhost/users'


settings = Settings()
