from common.utils import OSSAPI_GAMEMODES, download_beatmap, _try_multiple
from common.database.objects import DBBeatmapset, DBBeatmap
from common.database.wrapper import session_wrapper
from common.app import ossapi, database, config
from common.files import BinaryFile, exists
from common.logging import get_logger
from ossapi import Beatmap, Beatmapset
from typing import Tuple

from sqlalchemy.orm import Session

import common.servers as servers
import time

logger = get_logger("repos.beatmaps")

def _get_username(user_id: int) -> str:
    try:
        if (user := ossapi.user(user_id)):
            return user.username
    except ValueError:
        pass
    return None

def _from_api_beatmap(beatmap: Beatmap) -> DBBeatmap:
    if not download_beatmap(beatmap.id, check_MD5=beatmap.checksum):
        logger.warn(f"Failed to download beatmap {beatmap.id}!")
    dbmap = DBBeatmap(
        id=beatmap.id,
        set_id=beatmap.beatmapset_id,
        mode=OSSAPI_GAMEMODES[beatmap.mode.value],
        md5=beatmap.checksum,
        version=beatmap.version,
        last_update=beatmap.last_updated,
        max_combo=beatmap.max_combo,
        bpm=beatmap.bpm,
        cs=beatmap.cs,
        od=beatmap.accuracy,
        ar=beatmap.ar,
        hp=beatmap.drain,
        diff=beatmap.difficulty_rating,
        total_length=beatmap.total_length,
        hit_length=beatmap.hit_length,
        count_circles=beatmap.count_circles,
        count_sliders=beatmap.count_sliders,
        count_spinners=beatmap.count_spinners,
    )
    dbmap.status = {
        'bancho': beatmap.status.value
    }
    for server in servers.servers:
        if server.server_name == 'bancho':
            continue
        dbmap.status[server.server_name] = server.get_map_status(beatmap.id)
    return dbmap

def _from_api_beatmapset(beatmapset: Beatmapset) -> DBBeatmapset:
    dbset = DBBeatmapset(
        id=beatmapset.id,
        artist=beatmapset.artist,
        artist_unicode=beatmapset.artist_unicode,
        title=beatmapset.title,
        title_unicode=beatmapset.title_unicode,
        source=beatmapset.source,
        mapper=beatmapset.creator,
        tags=beatmapset.tags.split(" "),
        pack_tags=beatmapset.pack_tags,
        nsfw=beatmapset.nsfw,
        video=beatmapset.video,
        spotlight=beatmapset.spotlight,
        availability=not beatmapset.availability.download_disabled,
        ranked_date=beatmapset.ranked_date,
        submitted_date=beatmapset.submitted_date
    )
    if beatmapset.genre:
        dbset.genre = beatmapset.genre['name']
    if beatmapset.language:
        dbset.language = beatmapset.language['name']
    noms = []
    if beatmapset.current_nominations:
        for nom in beatmapset.current_nominations:
            if (nom_user := _get_username(nom.user_id)):
                noms.append(nom_user)
    dbset.nominators = {
        'bancho': noms,
        'akatsuki': [],
        'titanic': []
    }
    return dbset

@session_wrapper
def get_beatmapset(beatmapset_id: int, force_fetch: bool = False, session: Session | None = None) -> DBBeatmapset | None:
    if (dbset := session.query(DBBeatmapset).filter(DBBeatmapset.id == beatmapset_id).first()) and not force_fetch:
        return dbset
    else:
        try:
            beatmapset = _try_multiple(ossapi.beatmapset, beatmapset_id)
            dbset = _from_api_beatmapset(beatmapset)
            session.merge(dbset)
            for beatmap in beatmapset.beatmaps:
                session.merge(_from_api_beatmap(beatmap))
            session.commit()
            time.sleep(0.4)
            return dbset
        except:
            logger.exception(f"Failed to get beatmapset {beatmapset_id}")
            return None

@session_wrapper
def get_beatmap(beatmap_id: int, force_fetch: bool = False, session: Session | None = None) -> DBBeatmap | None:
    if (dbmap := session.query(DBBeatmap).filter(DBBeatmap.id == beatmap_id).first()) and not force_fetch:
        session.expunge(dbmap.beatmapset)
        return dbmap
    else:
        try:
            beatmap = _try_multiple(ossapi.beatmap, beatmap_id)
            if get_beatmapset(beatmap.beatmapset_id, force_fetch=force_fetch, session=session):
                session.commit()
                beatmap = session.get(DBBeatmap, (beatmap_id))
                session.expunge(beatmap.beatmapset)
                return beatmap
        except:
            logger.exception(f"Failed to get beatmap {beatmap_id}")
            return None
            
def get_beatmap_file(beatmap_id: int) -> Tuple[bytes, str]:
    if not get_beatmap(beatmap_id):
        return None
    file = BinaryFile(f"{config.storage}/beatmaps/{beatmap_id}.osu.gz")
    if not file.exists():
        return
    file.load_data()
    return file.data, file.get_hash()
