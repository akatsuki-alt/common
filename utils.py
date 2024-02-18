from common.logging import get_logger
from common.constants import Mods

from common.files import BinaryFile, exists
from common.app import config

from datetime import datetime, timedelta
from typing import Optional

import requests
import math
import time

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
        if result := _catboy_download(beatmap_id):
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

def _catboy_download(beatmap_id) -> bool:
    response = requests.get(
        f"https://catboy.best/osu/{beatmap_id}",
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

def _try_multiple(func, args, _retries=3, _delay=1) -> Optional[object]:
    tries = 0
    while tries < _retries:
        try:
            if type(args) == dict:
                return func(**args)
            else:
                return func(args)
        except Exception as e:
            logger.exception(f"Failed to get {func.__name__} {args} ({e})")
            tries += 1
            time.sleep(_delay)
    return None

class Schedule:
    
    def __init__(self, hours: int, minutes: int, seconds: int) -> None:
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
    
    def current_delta(self) -> timedelta:
        now = datetime.now()
        return (datetime(now.year, now.month, now.day, self.hours, self.minutes, self.seconds) - now)

class MapStats:
    
    OD0_MS = 80
    OD10_MS = 20
    AR0_MS = 1800.0
    AR5_MS = 1200.0
    AR10_MS = 450.0
    OD_MS_STEP = (OD0_MS - OD10_MS) / 10.0
    AR_MS_STEP1 = (AR0_MS - AR5_MS) / 5.0
    AR_MS_STEP2 = (AR5_MS - AR10_MS) / 5.0

    def __init__(self, mods: int, ar: float, od: float, hp: float, cs: float, bpm: float) -> None:
        self.ar = ar
        self.od = od
        self.hp = hp
        self.cs = cs
        self.bpm = bpm
        self.mods = Mods(mods).members
        
        speed = 1
        od_ar_hp_multiplier = 1.0
        
        if Mods.DoubleTime in self.mods or Mods.Nightcore in self.mods:
            speed = 1.5
        
        if Mods.HalfTime in self.mods:
            speed = 0.75

        self.bpm *= speed
        
        if Mods.HardRock in self.mods:
            od_ar_hp_multiplier = 1.4
            self.cs = min(self.cs*1.3, 10)

        if Mods.Easy in self.mods:
            od_ar_hp_multiplier = 0.5
            self.cs *= 0.5
        
        self.ar *= od_ar_hp_multiplier
        self.hp = min(10, self.hp * od_ar_hp_multiplier)
        
        if self.ar < 5:
            arms = self.AR0_MS - self.AR_MS_STEP1 * self.ar
        else:
            arms = self.AR5_MS - self.AR_MS_STEP2 * (self.ar - 5)
        
        arms = min(self.AR0_MS, max(self.AR10_MS, arms)) / speed

        if arms > self.AR5_MS:
            self.ar = (self.AR0_MS - arms) / self.AR_MS_STEP1
        else:
            self.ar = 5.0 + (self.AR5_MS - arms) / self.AR_MS_STEP2
        
        odms = self.OD0_MS - math.ceil(self.OD_MS_STEP * self.od)
        odms /= speed
        self.od = (self.OD0_MS - odms) / self.OD_MS_STEP
