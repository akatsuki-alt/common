from common.database.objects import *
from dataclasses import dataclass
from typing import List

import datetime

@dataclass
class Score:

    id: int = 0
    user_id: int = 0
    server: str = None
    beatmap_id: int = 0
    beatmap_md5: str = None
    
    max_combo: int = 0
    full_combo: bool = False
    count_300: int = 0
    count_100: int = 0
    count_50: int = 0
    count_miss: int = 0
    count_katu: int = 0
    count_geki: int = 0
    accuracy: float = 0.0
    rank: str = None
    pp: float = 0.0
    score: int = 0
    mods: int = 0
    mode: int = 0
    relax: int = 0
    completed: int = 0
    pinned: bool = False
    date: datetime = None
    
    pp_system: str = None
    extra_metadata: dict = None

    def to_db(self) -> DBScore:
        return DBScore(
            id = self.id,
            user_id = self.user_id,
            server = self.server,
            beatmap_id = self.beatmap_id,
            beatmap_md5 = self.beatmap_md5,
            max_combo = self.max_combo,
            full_combo = self.full_combo,
            count_300 = self.count_300,
            count_100 = self.count_100,
            count_50 = self.count_50,
            count_miss = self.count_miss,
            count_katu = self.count_katu,
            count_geki = self.count_geki,
            accuracy = self.accuracy,
            rank = self.rank,
            pp = self.pp,
            score = self.score,
            mods = self.mods,
            mode = self.mode,
            relax = self.relax,
            completed = self.completed,
            pinned = self.pinned,
            date = self.date,
            last_updated = datetime.datetime.now(),
            pp_system = self.pp_system,
            extra_metadata = self.extra_metadata
        )

class ServerAPI:
    
    def __init__(self, server_name, pp_system):
        self.server_name = server_name
        self.pp_system = pp_system

    def get_user_best(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score]:
        return None
    
    def get_user_1s(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score]:
        return None
    
    def get_user_recent(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score]:
        return None