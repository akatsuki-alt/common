from common.api.server_api import *
from common.app import ossapi
from typing import List
from ossapi import ScoreType, GameMode

from ossapi import Score as OssapiScore


class BanchoAPI(ServerAPI):
    
    def __init__(self):
        super().__init__("bancho", "bancho-2022")
  
    def _mode(self, mode: int):
        return [GameMode.OSU, GameMode.TAIKO, GameMode.CATCH, GameMode.MANIA][mode]
      
    def _convert_score(self, score: OssapiScore) -> Score:
        if score.weight:
            pp = score.weight.pp * 100/score.weight.percentage # Dear god
        else:
            pp = ossapi.score(mode=score.mode, score_id=score.id).pp
        return Score(
            id = score.id,
            user_id = score.user().id,
            server = self.server_name,
            beatmap_id = score.beatmap.id,
            beatmap_md5 = score.beatmap.checksum,
            max_combo = score.max_combo,
            full_combo = score.perfect,
            count_300 = score.statistics.count_300,
            count_100 = score.statistics.count_100,
            count_50 = score.statistics.count_50,
            count_miss = score.statistics.count_miss,
            count_katu = score.statistics.count_katu,
            count_geki = score.statistics.count_geki,
            accuracy = score.accuracy*100,
            rank = score.rank.value,
            pp = pp,
            score = score.score,
            mods = score.mods.value,
            mode = score.mode_int,
            relax = 0,
            completed = 1 if not score.passed else 3, # ??
            pinned=score.current_user_attributes['pin'] is not None,
            date=score.created_at,
            pp_system=self.pp_system
        )
        
    def get_user_best(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score] | None:
        return [self._convert_score(score) for score in ossapi.user_scores(user_id, mode=self._mode(mode), offset=(page-1)*length, limit=length, type=ScoreType.BEST)]
    
    def get_user_1s(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score] | None:
        return [self._convert_score(score) for score in ossapi.user_scores(user_id, mode=self._mode(mode), offset=(page-1)*length, limit=length, type=ScoreType.FIRSTS)]

    def get_user_recent(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score] | None:
        return [self._convert_score(score) for score in ossapi.user_scores(user_id, mode=self._mode(mode), offset=(page-1)*length, limit=length, type=ScoreType.RECENT)]

    