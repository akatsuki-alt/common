from .database.postgres import Postgres
from ossapi import Ossapi
from config import Config

STOPPED = False

config = Config()
database = Postgres(config.postgres_user, config.postgres_password, config.postgres_host, config.postgres_port)
ossapi = Ossapi(config.ossapi_id, config.ossapi_secret)

