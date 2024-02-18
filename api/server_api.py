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

    def get_total_hits(self):
        return self.count_300 + self.count_100 + self.count_50 + self.count_miss

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
    medals_unlocked: int = 0
    banned: bool = False
    is_bot: bool = False
    
    extra_metadata: dict = None
    
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
            medals_unlocked = self.medals_unlocked,
            banned = self.banned,
            is_bot = self.is_bot,
            extra_metadata = self.extra_metadata
        )

@dataclass
class Stats:
    
    server: str = None
    user_id: int = 0
    mode: int = 0
    relax: int = 0
    date: Date = datetime.date.today()
    
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
    
    score: float = 0.0
    leaderboard_type: str = "pp"
    
    extra_metadata: dict = None
    
    def to_db(self) -> DBStats:
        return DBStats(
            server=self.server,
            user_id=self.user_id,
            mode=self.mode,
            relax=self.relax,
            date = self.date,
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
            d_rank=self.d_rank,
            extra_metadata=self.extra_metadata
        )        

    def to_db_compact(self) -> DBStatsCompact:
        return DBStatsCompact(
            id=self.user_id,
            server=self.server,
            leaderboard_type=self.leaderboard_type,
            mode=self.mode,
            relax=self.relax,
            global_rank=self.global_rank,
            country_rank=self.country_rank,
            score=self.score,
            pp=self.pp,
            ranked_score=self.ranked_score,
            total_score=self.total_score,
            play_count=self.play_count,
            replays_watched=self.replays_watched,
            total_hits=self.total_hits,
            accuracy=self.accuracy
        )

@dataclass
class Clan:
    
    id: int = 0
    server: str = None
    owner: int = 0
    name: str = None
    tag: str = None
    description: str = None
    icon: str = None
    status: int = 0
    
    def to_db(self) -> DBClan:
        return DBClan(
            id=self.id,
            server=self.server,
            owner=self.owner,
            name=self.name,
            tag=self.tag,
            description=self.description,
            icon=self.icon,
            status=self.status
        )

@dataclass
class ClanStats:
    
    id: int = 0
    server: str = None
    mode: int = 0
    relax: int = 0
    ranked_score: int = 0
    total_score: int = 0
    play_count: int = 0
    replays_watched: int = 0
    total_hits: int = 0
    accuracy: float = 0.0
    pp: float = 0.0
    first_places: int = 0
    rank_pp: int = 0
    rank_1s: int = 0
    
    def to_db(self) -> DBClanStats:
        return DBClanStats(
            id=self.id,
            server=self.server,
            mode=self.mode,
            relax=self.relax,
            ranked_score=self.ranked_score,
            total_score=self.total_score,
            play_count=self.play_count,
            replays_watched=self.replays_watched,
            total_hits=self.total_hits,
            accuracy=self.accuracy,
            pp=self.pp,
            first_places=self.first_places,
            rank_pp=self.rank_pp,
            rank_1s=self.rank_1s
        )
        
    def to_db_compact(self) -> DBClanStatsCompact:
        return DBClanStatsCompact(
            id=self.id,
            server=self.server,
            mode=self.mode,
            relax=self.relax,
            ranked_score=self.ranked_score,
            total_score=self.total_score,
            play_count=self.play_count,
            accuracy=self.accuracy,
            pp=self.pp,
            first_places=self.first_places,
            rank_pp=self.rank_pp,
            rank_1s=self.rank_1s
        )

@dataclass
class MapPlaycount:
    
    user_id: int
    server: str
    beatmap_id: int
    play_count: int
    
    def to_db(self) -> DBMapPlaycount:
        return DBMapPlaycount(
            user_id=self.user_id,
            server=self.server,
            beatmap_id=self.beatmap_id,
            play_count=self.play_count
        )

class SortType(Enum):
    PP = "pp"
    SCORE = "score"

@dataclass    
class ServerAPI:
    
    server_name: str = None
    supports_rx: bool = False
    supports_clans: bool = False

    def get_pp_system(self, mode: int, relax: int) -> str:
        return

    def get_user_best(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score] :
        return None
    
    def get_user_1s(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score]:
        return None
    
    def get_user_recent(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score]:
        return None

    def get_user_pinned(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score]:
        return None

    def get_user_most_played(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[MapPlaycount]:
        return None
    
    def get_user_info(self, user_id: int | str) -> Tuple[User, List[Stats]] | None:
        return None

    def get_map_status(self, beatmap_id: int) -> int:
        return -2
    
    def get_leaderboard(self, mode: int, relax: int, page: int, length: int, inactive = False, sort: SortType = SortType.PP) -> List[Tuple[User, Stats]] | None:
        return None
    
    def get_clan_info(self, clan_id: int, mode: int, relax: int) -> Tuple[Clan, ClanStats] | None:
        return None
    
    def get_clan_leaderboard(self, mode: int, relax: int, page: int, length: int) -> List[Tuple[Clan, ClanStats]] | None:
        return None

    def get_clan_leaderboard_1s(self, mode: int, relax: int, page: int, length: int) -> List[Tuple[Clan, ClanStats]] | None:
        return None

    def ping_server(self) -> bool:
        return False