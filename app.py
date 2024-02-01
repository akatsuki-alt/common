from .database.postgres import Postgres
from ossapi import Ossapi

import config

STOPPED = False

database = Postgres()
ossapi: Ossapi(config.OSSAPI_ID, config.OSSAPI_SECRET)

