from common.performance import performance_systems
from common.api.server_api import *
from common.utils import try_get

from typing import List, Tuple

import requests
import time

class AkatsukiAPI(ServerAPI):
    
    def __init__(self):
        super().__init__("akatsuki", supports_rx=True, supports_clans=True)
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
            pp_system=self.get_pp_system(json['play_mode'], relax),
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

    def _convert_stats(self, json: dict, user_id: int, mode: int, relax: int, leaderboard_type = "pp") -> Stats: 
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
    
    def _convert_clan_compact(self, json: dict):
        if 'id' in json: # Performance
            return Clan(server=self.server_name, id=json['id'], name=json['name'])
        else: # First places
            return Clan(
                server=self.server_name,
                id = json['clan'],
                name = json['name'],
                tag = json['tag']
            )
    
    def _convert_clan(self, json: dict):
        return Clan(
            server=self.server_name,
            id = json['id'],
            name = json['name'],
            tag = json['tag'],
            description = json['description'],
            icon = json['icon'],
            owner = json['owner'],
            status = json['status']
        )
    
    def _convert_clan_stats(self, json: dict, clan_id: int, mode: int, relax: int, fp_rank=0) -> ClanStats:
        if 'count' in json:
            return ClanStats(
                id = clan_id,
                server = self.server_name,
                mode = mode,
                relax = relax,
                first_places=json['count'],
                rank_1s=fp_rank
            )
        return ClanStats(
            id = clan_id,
            server = self.server_name,
            mode = mode,
            relax = relax,
            ranked_score=json['ranked_score'],
            total_score=json['total_score'],
            play_count=json['playcount'],
            replays_watched=json['replays_watched'],
            total_hits=json['total_hits'],
            accuracy=json['accuracy'],
            pp=json['pp'],
            rank_pp=json['global_leaderboard_rank'],
            rank_1s=fp_rank
        )
    
    def _convert_most_played(self, json, user_id: int) -> MapPlaycount:
        return MapPlaycount(
            user_id=user_id,
            server=self.server_name,
            beatmap_id=json['beatmap']['beatmap_id'],
            play_count=json['playcount']
        )
        
    def _lookup_user(self, username: str) -> int:
        req = self._get(f"https://akatsuki.gg/api/v1/users/lookup?name={username}")
        if not req.ok:
            return 0
        for lookup in req.json()['users']:
            if lookup['username'].lower() == username.lower():
                return lookup['id']
        return 0

    def get_pp_system(self, mode: int, relax: int) -> str:
        if relax > 0:
            return performance_systems['akatsuki'].name
        else:
            return performance_systems['bancho'].name

    def get_user_best(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score] | None:
        req = self._get(f"https://akatsuki.gg/api/v1/users/scores/best?mode={mode}&p={page}&l={min(length, 100)}&rx={relax}&id={user_id}")
        if not req.ok:
            return
        scores = req.json()['scores']
        if not scores:
            return
        return [self._convert_score(json, user_id, relax) for json in scores]

    def get_user_1s(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score]:
        req = self._get(f"https://akatsuki.gg/api/v1/users/scores/first?mode={mode}&p={page}&l={min(length, 100)}&rx={relax}&id={user_id}")
        if not req.ok:
            return []
        scores = req.json()['scores']
        if not scores:
            return []
        return [self._convert_score(json, user_id, relax) for json in scores]
    
    def get_user_recent(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score]:
        req = self._get(f"https://akatsuki.gg/api/v1/users/scores/recent?mode={mode}&p={page}&l={min(length, 100)}&rx={relax}&id={user_id}")
        if not req.ok:
            return []
        scores = req.json()['scores']
        if not scores:
            return []
        return [self._convert_score(json, user_id, relax) for json in scores]
    
    def get_user_pinned(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[Score]:
        req = self._get(f"https://akatsuki.gg/api/v1/users/scores/pinned?mode={mode}&p={page}&l={min(length, 100)}&rx={relax}&id={user_id}")
        if not req.ok:
            return []
        scores = req.json()['scores']
        if not scores:
            return []
        return [self._convert_score(json, user_id, relax) for json in scores]
    
    def get_user_most_played(self, user_id: int, mode: int, relax: int, page: int = 1, length: int = 100) -> List[MapPlaycount]:
        req = self._get(f"https://akatsuki.gg/api/v1/users/most_played?mode={mode}&p={page}&l={min(length, 100)}&rx={relax}&id={user_id}")
        if not req.ok:
            return []
        most_played = req.json()['most_played_beatmaps']
        if not most_played:
            return []
        return [self._convert_most_played(json, user_id) for json in most_played]
    
    def get_user_info(self, user_id: int | str) -> Tuple[User, List[Stats]] | None:
        if type(user_id) == str:
            user_id = self._lookup_user(user_id)
            if not user_id:
                return None, None
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

    def get_map_status(self, beatmap_id: int) -> int:
        req = self._get(f"https://akatsuki.gg/api/v1/beatmaps?b={beatmap_id}")
        if not req.ok:
            return -2
        return req.json()['ranked']-1
    
    def get_leaderboard(self, mode: int, relax: int, page: int, length: int, inactive=False, sort: SortType = SortType.PP) -> List[Tuple[User, Stats]] | None:
        length = min(length, 500)
        sort_type = sort
        if inactive and sort_type == "pp":
            sort_type = "magic" # Idk what this does but it works
        req = self._get(f"https://akatsuki.gg/api/v1/leaderboard?mode={mode}&p={page}&l={length}&rx={relax}&sort={sort_type}")
        if not req.ok:
            return
        users = req.json()['users']
        if not users:
            return
        return [(self._convert_user(data), self._convert_stats(data['chosen_mode'], data['id'], mode, relax, sort)) for data in users]
    
    def get_clan_info(self, clan_id: int, mode: int, relax: int) -> Tuple[Clan, ClanStats] | None:
        req = self._get(f"https://akatsuki.gg/api/v1/clans/stats?id={clan_id}&m={mode}&rx={relax}")
        if not req.ok:
            return
        return self._convert_clan(req.json()['clan']), self._convert_clan_stats(req.json()['clan']['chosen_mode'], req.json()['clan']['id'], mode, relax)
            
    def get_clan_leaderboard(self, mode: int, relax: int, page: int, length: int) -> List[Tuple[Clan, ClanStats]] | None:
        req = self._get(f"https://akatsuki.gg/api/v1/clans/stats/all?m={mode}&p={page}&l={min(length, 100)}&rx={relax}")
        if not req.ok:
            return
        return [(self._convert_clan_compact(data), self._convert_clan_stats(data['chosen_mode'], data['id'], mode, relax)) for data in req.json()['clans']]

    def get_clan_leaderboard_1s(self, mode: int, relax: int, page: int, length: int) -> List[Tuple[Clan, ClanStats]] | None:
        length = min(length, 100)
        req = self._get(f"https://akatsuki.gg/api/v1/clans/stats/first?m={mode}&p={page}&l={length}&rx={relax}")
        if not req.ok:
            return
        rank_offset = ((page-1)*length)+1
        data = req.json()['clans']
        return [(self._convert_clan_compact(data[x]), self._convert_clan_stats(data[x], data[x]['clan'], mode, relax, x+rank_offset)) for x in range(len(data))]

    def ping_server(self) -> bool:
        return self._get(f"https://akatsuki.gg/api/v1/ping").ok