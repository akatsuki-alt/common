from common.api.server_api import *

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

    def get_user_best(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score]:
        req = self._get(f"https://akatsuki.gg/api/v1/users/scores/best?mode={mode}&p={page}&l={min(length, 100)}&rx={relax}&id={user_id}")
        if not req.ok:
            return
        return [self._convert_score(json, user_id, relax) for json in req.json()['scores']]

    def get_user_1s(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score]:
        req = self._get(f"https://akatsuki.gg/api/v1/users/scores/first?mode={mode}&p={page}&l={min(length, 100)}&rx={relax}&id={user_id}")
        if not req.ok:
            return
        return [self._convert_score(json, user_id, relax) for json in req.json()['scores']]
    
    def get_user_recent(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score]:
        req = self._get(f"https://akatsuki.gg/api/v1/users/scores/recent?mode={mode}&p={page}&l={min(length, 100)}&rx={relax}&id={user_id}")
        if not req.ok:
            return
        return [self._convert_score(json, user_id, relax) for json in req.json()['scores']]
        