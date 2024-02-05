from common.api.akatsuki import AkatsukiAPI
from common.api.titanic import TitanicAPI
from common.api.bancho import BanchoAPI

from common.api.server_api import ServerAPI

from typing import List

servers = [AkatsukiAPI(), BanchoAPI(), TitanicAPI()]

def by_name(name: str) -> ServerAPI | None:
    for server in servers:
        if server.server_name == name:
            return server
    return None
