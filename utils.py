from datetime import datetime, timedelta

from .files import BinaryFile, exists
from .app import config

import requests
import logging

OSSAPI_GAMEMODES = {'osu': 0, 'taiko': 1, 'fruits': 2, 'mania': 3}
DEFAULT_HEADERS = {"user-agent": "akatsukialt!/KompirBot fetch service"}
logger = logging.getLogger("utils")

def download_beatmap(beatmap_id, check_MD5: str = None, force_download=False) -> bool:
    if exists(f"{config.storage}/beatmaps/{beatmap_id}.osu.gz") and not force_download:
        if check_MD5:
            local_MD5 = BinaryFile(f"{config.storage}/beatmaps/{beatmap_id}.osu.gz").get_hash()
            if local_MD5 != check_MD5:
                logger.warning(f"Found mismatch in MD5 for beatmap {beatmap_id} (local: {local_MD5}, remote: {check_MD5})")
                return download_beatmap(beatmap_id, force_download=True)
        return True
    if result := _osudirect_download(beatmap_id):
        return result

    # Use old.ppy.sh as backup endpoint
    return _ppy_download(beatmap_id)


def _osudirect_download(beatmap_id) -> bool:
    response = requests.get(
        f"https://osu.direct/api/osu/{beatmap_id}",
        headers=DEFAULT_HEADERS,
    )
    if not response.ok:
        logger.warning(f"GET {response.url} {response.status_code}")
        #logger.warning(f"{response.text}")
        return False
    #logger.info(f"GET {response.url} {response.status_code}")
    file = BinaryFile(f"{config.storage}/beatmaps/{beatmap_id}.osu.gz")
    file.data = response.content
    file.save_data()
    return True

def _ppy_download(beatmap_id) -> bool:
    response = requests.get(
        f"https://old.ppy.sh/osu/{beatmap_id}",
        headers=DEFAULT_HEADERS,
    )
    if not response.ok or not response.content:
        logger.warning(f"GET {response.url} {response.status_code}")
        logger.warning(f"{response.text}")
        return False
    logger.info(f"GET {response.url} {response.status_code}")
    file = BinaryFile(f"{config.storage}/beatmaps/{beatmap_id}.osu.gz")
    file.data = response.content
    file.save_data()
    return True

class Schedule:
    
    def __init__(self, hours: int, minutes: int, seconds: int) -> None:
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
    
    def current_delta(self) -> timedelta:
        now = datetime.now()
        return (datetime(now.year, now.month, now.day, self.hours, self.minutes, self.seconds) - now)