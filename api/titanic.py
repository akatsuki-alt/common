from common.performance import performance_systems
from common.api.server_api import *

from typing import List, Tuple

import requests
import time

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"

class TitanicAPI(ServerAPI):
    
    def __init__(self):
        super().__init__("titanic", supports_lb_tracking=True)
        self._last_response = time.time()
    
    def _get(self, url) -> requests.Response:
        delta = time.time() - self._last_response
        delay = 60/120
        if delta < delay:
            time.sleep(delay - delta)
        self._last_response = time.time()
        return requests.get(url)

    def _convert_user(self, json: dict) -> User:
        return User(
            id=json['id'],
            server=self.server_name,
            username=json['name'],
            username_history=[item['name'] for item in json['names']],
            country=json['country'],
            registered_on=datetime.datetime.strptime(json['created_at'], DATE_FORMAT),
            latest_activity=datetime.datetime.strptime(json['latest_activity'], DATE_FORMAT),
            favourite_mode=json['preferred_mode'],
            banned=json['restricted'],
            extra_metadata={'groups': [group['group_id'] for group in json['groups']]}
        )

    def _convert_stats(self, json: dict, user_id: int, leaderboard_type="pp") -> Stats:
        score = 0
        if leaderboard_type == "pp":
            score=json['pp']
        elif leaderboard_type == "score":
            score=json['ranked_score']
        return Stats(
            server=self.server_name,
            leaderboard_type=leaderboard_type,
            score=score,
            user_id=user_id,
            mode=json['mode'],
            relax=0,
            ranked_score=json['rscore'],
            total_score=json['tscore'],
            play_count=json['playcount'],
            play_time=json['playtime'],
            replays_watched=json['replay_views'],
            total_hits=json['total_hits'],
            max_combo=json['max_combo'],
            level=0, # TODO
            accuracy=json['acc']*100,
            pp=json['pp'],
            global_rank=json['rank'],
            country_rank=-1, # TODO
            global_score_rank=-1, # TODO
            country_score_rank=-1, # TODO
            xh_rank=json['xh_count'],
            x_rank=json['x_count'],
            sh_rank=json['sh_count'],
            s_rank=json['s_count'],
            a_rank=json['a_count'],
            b_rank=json['b_count'],
            c_rank=json['c_count'],
            d_rank=json['d_count'],
            clears=sum([x for x in json.keys() if x.startswith('count_')]),
            followers=-1,
            medals_unlocked=-1, # TODO
            extra_metadata={'ppv1': json['ppv1']}
        )

    def _convert_score(self, json: dict, user_id: int, relax: int):
        return Score(
            id=json['id'],
            user_id=user_id,
            server=self.server_name,
            beatmap_md5=json['beatmap']['md5'],
            beatmap_id=json['beatmap']['id'],
            max_combo=json['max_combo'],
            full_combo=json['perfect'],
            count_300=json['n300'],
            count_100=json['n100'],
            count_50=json['n50'],
            count_miss=json['nMiss'],
            count_geki=json['nGeki'],
            count_katu=json['nKatu'],
            accuracy=json['acc']*100,
            rank=json['grade'],
            pp=json['pp'],
            score=json['total_score'],
            mods=json['mods'],
            mode=json['mode'],
            relax=0,
            completed=json['status'],
            pinned=json['pinned'],
            date=datetime.datetime.strptime(json['submitted_at'], DATE_FORMAT),
            pp_system=self.get_pp_system(json['mode'], relax),
            extra_metadata=None
        )
        
    def _convert_most_played(self, json: dict, user_id: int) -> MapPlaycount:
        return MapPlaycount(
            user_id=user_id,
            server=self.server_name,
            beatmap_id=json['beatmap']['id'],
            play_count=json['count']
        )

    def get_pp_system(self, mode: int, relax: int) -> str:
        return performance_systems['titanic'].name

    def get_user_best(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 50) -> List[Score]:
        length = min(length, 50)
        mode = ['osu', 'taiko', 'fruits', 'mania'][mode]
        req = self._get(f"https://osu.lekuru.xyz/api/profile/{user_id}/top/{mode}?limit={length}&offset={length*(page-1)}")
        scores = req.json()
        if not scores:
            return []
        return [self._convert_score(json, user_id, relax) for json in scores]

    def get_user_1s(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 50) -> Tuple[List[Score], int]:
        length = min(length, 50)
        mode = ['osu', 'taiko', 'fruits', 'mania'][mode]
        req = self._get(f"https://osu.lekuru.xyz/api/profile/{user_id}/first/{mode}?limit={length}&offset={length*(page-1)}")
        if not req.ok:
            return []
        scores = req.json()
        if not scores:
            return []
        return [self._convert_score(json, user_id, relax) for json in scores], len(scores) # TODO

    def get_user_recent(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 50) -> List[Score]:
        length = min(length, 50)
        mode = ['osu', 'taiko', 'fruits', 'mania'][mode]
        req = self._get(f"https://osu.lekuru.xyz/api/profile/{user_id}/recent/{mode}?limit={length}&offset={length*(page-1)}")
        if not req.ok:
            return []
        scores = req.json()
        if not scores:
            return []
        return [self._convert_score(json, user_id, relax) for json in scores]

    def get_user_pinned(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 50) -> List[Score]:
        length = min(length, 50)
        mode = ['osu', 'taiko', 'fruits', 'mania'][mode]
        req = self._get(f"https://osu.lekuru.xyz/api/profile/{user_id}/pinned/{mode}?limit={length}&offset={length*(page-1)}")
        if not req.ok:
            return []
        scores = req.json()
        if not scores:
            return []
        return [self._convert_score(json, user_id, relax) for json in scores]

    def get_user_most_played(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[MapPlaycount]:
        length = min(length, 50)
        #mode = ['osu', 'taiko', 'fruits', 'mania'][mode]
        req = self._get(f"https://osu.lekuru.xyz/api/profile/{user_id}/plays?limit={length}&offset={length*(page-1)}")
        if not req.ok:
            return []
        most_played = req.json()
        if not most_played:
            return []
        return [self._convert_most_played(json, user_id) for json in most_played]

    def get_user_info(self, user_id: int | str) -> Tuple[User, List[Stats]] | None:
        req = self._get(f"https://osu.lekuru.xyz/api/profile/{user_id}")
        if not req.ok:
            return None, None
        data = req.json()
        return self._convert_user(data), [self._convert_stats(stats, user_id) for stats in data['stats']]
    
    def get_leaderboard(self, mode: int, relax: int, page: int, length: int, inactive=False, sort: SortType = SortType.PP) -> List[Tuple[User, Stats]] | None:
        length = min(length, 50)
        sort_type = "performance"
        mode_str = ['osu', 'taiko', 'fruits', 'mania'][mode]
        if sort == SortType.SCORE:
            sort_type = "rscore"
        req = self._get(f"https://osu.lekuru.xyz/api/rankings/{sort_type}/{mode_str}?limit=50&offset={length*(page-1)}")
        if not req.ok:
            return None
        return [(self._convert_user(json['user']), self._convert_stats(json['user']['stats'][mode], json['user']['id'], sort)) for json in req.json()]
    
    def get_user_pfp(self, user_id: int) -> str:
        return f"https://osu.lekuru.xyz/a/{user_id}"
    
    def ping_server(self) -> bool:
        return self._get(f"https://osu.lekuru.xyz/").ok