from datetime import datetime, timedelta

from common.logging import get_logger

from common.files import BinaryFile, exists
from common.app import config

import requests

OSSAPI_GAMEMODES = {'osu': 0, 'taiko': 1, 'fruits': 2, 'mania': 3}
DEFAULT_HEADERS = {"user-agent": "akatsukialt!/KompirBot fetch service"}
logger = get_logger("utils")

def download_beatmap(beatmap_id, check_MD5: str = None, force_download=False, skip_mirror=False) -> bool:
    if exists(f"{config.storage}/beatmaps/{beatmap_id}.osu.gz") and not force_download:
        if check_MD5:
            local_MD5 = BinaryFile(f"{config.storage}/beatmaps/{beatmap_id}.osu.gz").get_hash()
            if local_MD5 != check_MD5:
                logger.warning(f"Found mismatch in MD5 for beatmap {beatmap_id} (local: {local_MD5}, remote: {check_MD5})")
                return download_beatmap(beatmap_id, force_download=True, skip_mirror=True)
        return True

    if not skip_mirror:
        if result := _osudirect_download(beatmap_id):
            local_MD5 = BinaryFile(f"{config.storage}/beatmaps/{beatmap_id}.osu.gz").get_hash()
            if check_MD5 and local_MD5 != check_MD5:
                logger.warning(f"Mirror likely have outdated beatmap for {beatmap_id} (local: {local_MD5}, remote: {check_MD5})")
            else:
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
    #logger.info(f"GET {response.url} {response.status_code}")
    file = BinaryFile(f"{config.storage}/beatmaps/{beatmap_id}.osu.gz")
    file.data = response.content
    file.save_data()
    return True

def try_get(dikt: dict, key: str, default=None):
    try:
        return dikt[key]
    except KeyError:
        return default

class Schedule:
    
    def __init__(self, hours: int, minutes: int, seconds: int) -> None:
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
    
    def current_delta(self) -> timedelta:
        now = datetime.now()
        return (datetime(now.year, now.month, now.day, self.hours, self.minutes, self.seconds) - now)