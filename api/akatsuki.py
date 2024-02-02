from common.api.server_api import *
from common.utils import try_get

import requests
import time

class AkatsukiAPI(ServerAPI):
    
    def __init__(self):
        super().__init__("akatsuki", "akatsuki-pp-rs_0.9.6")
        self._last_response = time.time()
    
    def _get(self, url) -> requests.Response:
        delta = time.time() - self._last_response
        delay = 60/120
        if delta < delay:
            time.sleep(delay - delta)
        self._last_response = time.time()
        return requests.get(url)

    def _convert_score(self, json: dict, user_id: int, relax: int) -> Score:
        return Score(
            id=int(json['id']),
            user_id=user_id,
            server=self.server_name,
            beatmap_md5=json['beatmap_md5'],
            beatmap_id=json['beatmap']['beatmap_id'],
            max_combo=json['max_combo'],
            full_combo=json['full_combo'],
            mods=json['mods'],
            count_300=json['count_300'],
            count_100=json['count_100'],
            count_50=json['count_50'],
            count_katu=json['count_katu'],
            count_geki=json['count_geki'],
            count_miss=json['count_miss'],
            accuracy=json['accuracy'],
            rank=json['rank'],
            pp=json['pp'],
            score=json['score'],
            mode=json['play_mode'],
            relax=relax,
            completed=json['completed'],
            date=datetime.datetime.fromisoformat(json['time']),
            pinned=json['pinned'],
            pp_system=self.pp_system
        )


    def _convert_user(self, json: dict) -> User:
        clan_id = json['clan']['id'] if 'clan' in json else -1
        return User(
            id = int(json['id']),
            clan_id=clan_id,
            server = self.server_name,
            username = json['username'],
            username_history = [json['username']],
            country = json['country'],
            registered_on = datetime.datetime.fromisoformat(json['registered_on']),
            latest_activity = datetime.datetime.fromisoformat(json['latest_activity']),
            favourite_mode = json['favourite_mode'],
            followers = try_get(json, 'followers', 0)
        )

    def _convert_stats(self, json: dict, user_id: int, mode: int, relax: int) -> Stats: 
        return Stats(
            server=self.server_name,
            user_id=user_id,
            mode=mode,
            relax=relax,
            ranked_score=json['ranked_score'],
            total_score=json['total_score'],
            play_count=json['playcount'],
            play_time=json['playtime'],
            max_combo=json['max_combo'],
            replays_watched=try_get(json, 'replays_watched', 0),
            total_hits=json['total_hits'],
            level=json['level'],
            accuracy=json['accuracy'],
            pp=json['pp'],
            global_rank=json['global_leaderboard_rank'],
            country_rank=json['country_leaderboard_rank'],
            global_score_rank=0, # TODO
            country_score_rank=0, # TODO
            xh_rank=0, # TODO
            x_rank=0, # TODO
            sh_rank=0, # TODO
            s_rank=0, # TODO
            a_rank=0, # TODO
            b_rank=0, # TODO
            c_rank=0, # TODO
            d_rank=0, # TODO
        )

    def get_user_best(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score] | None:
        req = self._get(f"https://akatsuki.gg/api/v1/users/scores/best?mode={mode}&p={page}&l={min(length, 100)}&rx={relax}&id={user_id}")
        if not req.ok:
            return
        return [self._convert_score(json, user_id, relax) for json in req.json()['scores']]

    def get_user_1s(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score] | None:
        req = self._get(f"https://akatsuki.gg/api/v1/users/scores/first?mode={mode}&p={page}&l={min(length, 100)}&rx={relax}&id={user_id}")
        if not req.ok:
            return
        return [self._convert_score(json, user_id, relax) for json in req.json()['scores']]
    
    def get_user_recent(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score] | None:
        req = self._get(f"https://akatsuki.gg/api/v1/users/scores/recent?mode={mode}&p={page}&l={min(length, 100)}&rx={relax}&id={user_id}")
        if not req.ok:
            return
        return [self._convert_score(json, user_id, relax) for json in req.json()['scores']]
    
    def get_user_info(self, user_id: int) -> Tuple[User, List[Stats]] | None:
        req = self._get(f"https://akatsuki.gg/api/v1/users/full?id={user_id}")
        if not req.ok:
            return None, None
        json = req.json()
        stats = list()
        modes = ['std', 'taiko', 'ctb', 'mania']
        for relax in range(3):
            max_mode = 4
            if relax == 1:
                max_mode = 3
            elif relax == 2:
                max_mode = 1
            for mode in range(max_mode):
                stats.append(self._convert_stats(json['stats'][relax][modes[mode]], user_id, mode, relax))
        return self._convert_user(json), stats