from common.database.objects import *
from dataclasses import dataclass
from typing import Tuple, List

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

@dataclass
class User:
    
    id: int = 0
    clan_id: int = 0
    server: str = None
    username: str = None
    username_history: List[str] = None
    country: str = None
    registered_on: datetime = None
    latest_activity: datetime = None
    favourite_mode: int = 0
    followers: int = 0
    banned: bool = False
    
    def to_db(self) -> DBUser:
        return DBUser(
            id = self.id,
            clan_id = self.clan_id,
            server = self.server,
            username = self.username,
            username_history = self.username_history,
            country = self.country,
            registered_on = self.registered_on,
            latest_activity = self.latest_activity,
            favourite_mode = self.favourite_mode,
            followers = self.followers,
            banned = self.banned
        )

@dataclass
class Stats:
    
    server: str = None
    user_id: int = 0
    mode: int = 0
    relax: int = 0
    
    ranked_score: int = 0
    total_score: int = 0
    play_count: int = 0
    play_time: int = 0
    replays_watched: int = 0
    total_hits: int = 0
    max_combo: int = 0
    level: float = 0.0
    accuracy: float = 0.0
    pp: float = 0.0
    
    global_rank: int = 0
    country_rank: int = 0
    global_score_rank: int = 0
    country_score_rank: int = 0
    
    xh_rank: int = 0
    x_rank: int = 0
    sh_rank: int = 0
    s_rank: int = 0
    a_rank: int = 0
    b_rank: int = 0
    c_rank: int = 0
    d_rank: int = 0 
    
    def to_db(self) -> DBStats:
        return DBStats(
            server=self.server,
            user_id=self.user_id,
            mode=self.mode,
            relax=self.relax,
            ranked_score=self.ranked_score,
            total_score=self.total_score,
            play_count=self.play_count,
            play_time=self.play_time,
            replays_watched=self.replays_watched,
            total_hits=self.total_hits,
            max_combo=self.max_combo,
            level=self.level,
            accuracy=self.accuracy,
            pp=self.pp,
            global_rank=self.global_rank,
            country_rank=self.country_rank,
            global_score_rank=self.global_score_rank,
            country_score_rank=self.country_score_rank,
            xh_rank=self.xh_rank,
            x_rank=self.x_rank,
            sh_rank=self.sh_rank,
            s_rank=self.s_rank,
            a_rank=self.a_rank,
            b_rank=self.b_rank,
            c_rank=self.c_rank,
            d_rank=self.d_rank
        )

class ServerAPI:
    
    def __init__(self, server_name, pp_system):
        self.server_name = server_name
        self.pp_system = pp_system

    def get_user_best(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score] | None:
        return None
    
    def get_user_1s(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score] | None:
        return None
    
    def get_user_recent(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score] | None:
        return None

    def get_user_info(self, user_id: int) -> Tuple[User, List[Stats]] | None:
        return None

    def get_map_status(self, beatmap_id: int) -> int:
        return -2