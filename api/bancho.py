from ossapi.models import UserStatistics, BeatmapPlaycount, UserCompact, Cursor
from ossapi import RankingType, ScoreType, GameMode, UserBeatmapType
from ossapi.models import User as Ossapi_User
from ossapi import Score as OssapiScore

from common.performance import performance_systems, SimulatedScore
from common.api.server_api import *
from common.app import ossapi


from typing import List, Tuple

class BanchoAPI(ServerAPI):
    
    def __init__(self):
        super().__init__("bancho")
  
    def _mode(self, mode: int):
        return [GameMode.OSU, GameMode.TAIKO, GameMode.CATCH, GameMode.MANIA][mode]
      
    def _convert_score(self, score: OssapiScore, recalc_pp: bool = False) -> Score:
        if score.weight:
            pp = score.weight.pp * 100/score.weight.percentage # Dear god
        elif score.id != 0:
            pp = ossapi.score(mode=score.mode, score_id=score.id).pp
        elif recalc_pp:
            pp = performance_systems['bancho'].simulate(SimulatedScore(
                beatmap_id = score.beatmap.id,
                mods = score.mods.value,
                max_combo = score.max_combo,
                n300 = score.statistics.count_300,
                n100 = score.statistics.count_100,
                n50 = score.statistics.count_50,
                nMiss = score.statistics.count_miss,
                nGeki = score.statistics.count_geki,
                nKatu = score.statistics.count_katu,
                mode = score.mode_int,
                passed_objects = score.statistics.count_300 + score.statistics.count_100 + score.statistics.count_50 + score.statistics.count_miss
            ))
        else:
            pp = 0
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
            pp_system=self.get_pp_system(score.mode_int, 0),
        )
        
    def _convert_stats(self, stats: UserStatistics, mode: int) -> Stats:
        return Stats(
            server=self.server_name,
            user_id=stats.user.id,
            mode=mode,
            relax=0,
            ranked_score=stats.ranked_score,
            total_score=stats.total_score,
            play_count=stats.play_count,
            play_time=stats.play_time,
            replays_watched=stats.replays_watched_by_others,
            total_hits=stats.total_hits,
            max_combo=stats.maximum_combo,
            level=stats.level.current + (stats.level.progress/100),
            accuracy=stats.hit_accuracy,
            pp=stats.pp,
            global_rank=stats.global_rank,
            country_rank=stats.country_rank, # Doesnt work on lb
            global_score_rank=-1, # TODO: score api
            country_score_rank=-1, # TODO: score api
            xh_rank=stats.grade_counts.ssh,
            x_rank=stats.grade_counts.ss,
            sh_rank=stats.grade_counts.sh,
            s_rank=stats.grade_counts.s,
            a_rank=stats.grade_counts.a,
            b_rank=-1, # TODO: use osu alt api for this
            c_rank=-1,
            d_rank=-1,
            clears=-1, 
            medals_unlocked=-1,
            first_places=-1,
            followers=stats.user.follower_count
        )
        
    def _convert_most_played(self, json: BeatmapPlaycount, user_id: int) -> MapPlaycount:
        return MapPlaycount(
            user_id=user_id,
            server=self.server_name,
            beatmap_id=json.beatmap_id,
            play_count=json.count
        )
    
    def _convert_user_compact(self, user: UserCompact) -> User:
        return User(
            id = user.id,
            server = self.server_name,
            username = user.username,
            username_history = [user.username],
            country = user.country_code,
            latest_activity = user.last_visit,
            banned = True if user.is_restricted else False, # Null for some reason
            is_bot = user.is_bot
        )
    
    def _convert_user(self, user: Ossapi_User) -> User:
        return User(
            id = user.id,
            server = self.server_name,
            username = user.username,
            username_history = [user.username],
            country = user.country_code,
            registered_on = user.join_date,
            latest_activity = user.last_visit,
            banned = True if user.is_restricted else False, # Null for some reason
            is_bot = user.is_bot,
        )
    
    def get_pp_system(self, mode: int, relax: int) -> str:
        return performance_systems['bancho'].name

    def get_user_best(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score] | None:
        return [self._convert_score(score) for score in ossapi.user_scores(user_id, mode=self._mode(mode), offset=(page-1)*length, limit=length, type=ScoreType.BEST)]
    
    def get_user_1s(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> Tuple[List[Score], int] | None:
        return [self._convert_score(score) for score in ossapi.user_scores(user_id, mode=self._mode(mode), offset=(page-1)*length, limit=length, type=ScoreType.FIRSTS)], ossapi.user(user_id).scores_first_count

    def get_user_recent(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score] | None:
        scores = ossapi.user_scores(user_id, mode=self._mode(mode), offset=(page-1)*length, limit=length, type=ScoreType.RECENT)
        if not scores:
            return []
        return [self._convert_score(scores[0])] + [self._convert_score(score, recalc_pp=False) for score in scores[1:]]

    def get_user_most_played(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[MapPlaycount] | None:
        return [self._convert_most_played(map, user_id) for map in ossapi.user_beatmaps(user_id, type=UserBeatmapType.MOST_PLAYED, offset=(page-1)*length, limit=length)]

    def get_user_info(self, user_id: int | str, mode: int | None = None, relax: int | None = None) -> Tuple[User, List[Stats]] | None:
        stats = []
        modes = [GameMode.OSU, GameMode.TAIKO, GameMode.CATCH, GameMode.MANIA]
        if mode is None:
            mode = 0
            for gamemode in modes:
                current_mode_profile = ossapi.user(user_id, mode=gamemode)
                if not current_mode_profile:
                    continue
                current_mode_profile.statistics.user = current_mode_profile
                stats.append(self._convert_stats(current_mode_profile.statistics, mode))
                mode += 1
        else:
            current_mode_profile = ossapi.user(user_id, mode=modes[mode])
            current_mode_profile.statistics.user = current_mode_profile
            stats.append(self._convert_stats(current_mode_profile.statistics, mode))
        return self._convert_user(current_mode_profile), stats

    def get_map_status(self, beatmap_id: int) -> int:
        try:
            return ossapi.beatmap(beatmap_id=beatmap_id).status.value
        except ValueError:
            return -2

    def get_leaderboard(self, mode: int, relax: int, page: int, length: int, inactive=False, sort: SortType = SortType.PP) -> List[Tuple[User, Stats]] | None:
        return [(self._convert_user_compact(stats.user), self._convert_stats(stats, mode)) for stats in ossapi.ranking(mode=self._mode(mode), type=RankingType.PERFORMANCE if sort == SortType.PP else RankingType.SCORE, cursor=Cursor(page=page, length=length)).ranking]

    def get_user_pfp(self, user_id: int) -> str:
        return f"https://a.ppy.sh/{user_id}"