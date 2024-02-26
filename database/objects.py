from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from datetime import datetime
from typing import Optional

from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy import *


Base = declarative_base()

class DBTask(Base):
    
    __tablename__ = "tasks"
    
    name = Column('name', String, primary_key=True)
    last_run = Column('last_run', DateTime)

class DBBeatmapset(Base):
    
    __tablename__ = 'beatmapsets'
    
    id = Column('id', Integer, primary_key=True)
    artist = Column('artist', String)
    artist_unicode = Column('artist_unicode', String)
    title = Column('title', String)
    title_unicode = Column('title_unicode', String)
    source = Column('source', String)
    mapper = Column('mapper', String)
    nominators = Column('nominators', JSONB)
    tags = Column('tags', ARRAY(String))
    pack_tags = Column('pack_tags', ARRAY(String))
    genre = Column('genre', String)
    language = Column('language', String)
    nsfw = Column('nsfw', Boolean)
    video = Column('video', Boolean)
    spotlight = Column('spotlight', Boolean)
    availability = Column('availability', Boolean)
    
    last_updated = Column('last_updated', DateTime(timezone=True), server_default=func.now())
    ranked_date = Column('ranked_date', DateTime(timezone=True))
    submitted_date = Column('submitted_date', DateTime(timezone=True))

    beatmaps   = relationship('DBBeatmap', back_populates='beatmapset')

    def get_url(self):
        return f"https://osu.ppy.sh/s/{self.id}"

class DBBeatmap(Base):
    
    __tablename__ = 'beatmaps'
        
    id = Column('id', Integer, primary_key=True)
    set_id = Column('set_id', Integer, ForeignKey('beatmapsets.id'))
    mode = Column('mode', SmallInteger)
    md5 = Column('md5', String)
    version = Column('version', String)
    last_update = Column('last_update', DateTime)
    max_combo = Column('max_combo', Integer)
    bpm = Column('bpm', Float)
    cs = Column('cs', Float)
    od = Column('od', Float)
    ar = Column('ar', Float)
    hp = Column('hp', Float)
    diff = Column('diff', Float)
    hit_length = Column('hit_length', Integer)
    total_length = Column('total_length', Integer)

    count_circles = Column('count_circles', Integer)
    count_sliders = Column('count_sliders', Integer)
    count_spinners = Column('count_spinners', Integer)

    status = Column('status', JSONB)
    
    last_db_update = Column('last_db_update', DateTime(timezone=True), default=datetime.now())
    beatmapset = relationship('DBBeatmapset', back_populates='beatmaps')

    def get_title(self):
        if not self.beatmapset:
            return self.version
        return f"{self.beatmapset.artist} - {self.beatmapset.title} [{self.version}]"
    
    def get_url(self):
        return f"https://osu.ppy.sh/b/{self.id}"

    def get_total_hits(self):
        return self.count_circles + self.count_sliders + self.count_spinners

class DBUser(Base):
    
    __tablename__ = 'users'
    
    id = Column('id', Integer, primary_key=True)
    clan_id = Column('clan_id', Integer)
    server = Column('server', String, primary_key=True)
    username = Column('username', String)
    username_history = Column('username_history', ARRAY(String))
    country = Column('country', String)
    registered_on = Column('registered', DateTime)
    latest_activity = Column('latest_activity', DateTime)
    favourite_mode = Column('favourite_mode', SmallInteger)
    banned = Column('banned', Boolean)
    is_bot = Column('is_bot', Boolean)
    
    extra_metadata = Column('extra_metadata', JSONB)

class DBStatsTemp(Base):

    __tablename__ = 'stats_temp'
    
    server = Column('server', String, primary_key=True)
    user_id = Column('user_id', Integer, primary_key=True)
    mode = Column('mode', SmallInteger, primary_key=True)
    relax = Column('relax', SmallInteger, primary_key=True)
    date = Column('date', DateTime, primary_key=True)
    
    ranked_score = Column('ranked_score', BigInteger)
    total_score = Column('total_score', BigInteger)
    play_count = Column('play_count', Integer)
    play_time = Column('play_time', Integer)
    replays_watched = Column('replays_watched', Integer)
    total_hits = Column('total_hits', Integer)
    max_combo = Column('max_combo', Integer)
    level = Column('level', Float)
    accuracy = Column('accuracy', Float)
    pp = Column('pp', Float)
    first_places = Column('first_places', Integer)
    
    global_rank = Column('global_rank', Integer)
    country_rank = Column('country_rank', Integer)
    global_score_rank = Column('global_score_rank', Integer)
    country_score_rank = Column('country_score_rank', Integer)
    
    xh_rank = Column('xh_rank', Integer)
    x_rank = Column('x_rank', Integer)
    sh_rank = Column('sh_rank', Integer)
    s_rank = Column('s_rank', Integer)
    a_rank = Column('a_rank', Integer)
    b_rank = Column('b_rank', Integer)
    c_rank = Column('c_rank', Integer)
    d_rank = Column('d_rank', Integer)
    clears = Column('clears', Integer)

    followers = Column('followers', Integer)
    medals_unlocked = Column('medals_unlocked', Integer)

    extra_metadata = Column('extra_metadata', JSONB)
    discord_id = Column('discord_id', BigInteger, primary_key=True)

class DBStats(Base):

    __tablename__ = 'stats'
    
    server = Column('server', String, primary_key=True)
    user_id = Column('user_id', Integer, primary_key=True)
    mode = Column('mode', SmallInteger, primary_key=True)
    relax = Column('relax', SmallInteger, primary_key=True)
    date = Column('date', Date, primary_key=True)
    
    ranked_score = Column('ranked_score', BigInteger)
    total_score = Column('total_score', BigInteger)
    play_count = Column('play_count', Integer)
    play_time = Column('play_time', Integer)
    replays_watched = Column('replays_watched', Integer)
    total_hits = Column('total_hits', Integer)
    max_combo = Column('max_combo', Integer)
    level = Column('level', Float)
    accuracy = Column('accuracy', Float)
    pp = Column('pp', Float)
    first_places = Column('first_places', Integer)
    global_rank = Column('global_rank', Integer)
    country_rank = Column('country_rank', Integer)
    global_score_rank = Column('global_score_rank', Integer)
    country_score_rank = Column('country_score_rank', Integer)
    
    xh_rank = Column('xh_rank', Integer)
    x_rank = Column('x_rank', Integer)
    sh_rank = Column('sh_rank', Integer)
    s_rank = Column('s_rank', Integer)
    a_rank = Column('a_rank', Integer)
    b_rank = Column('b_rank', Integer)
    c_rank = Column('c_rank', Integer)
    d_rank = Column('d_rank', Integer)
    clears = Column('clears', Integer)

    followers = Column('followers', Integer)
    medals_unlocked = Column('medals_unlocked', Integer)

    extra_metadata = Column('extra_metadata', JSONB)

    def copy(self, discord_id: int) -> DBStatsTemp:
        stats = DBStatsTemp()
        for k,v in self.__dict__.items():
            if k.startswith("_"):
                continue
            setattr(stats, k, v)
        stats.date = datetime.now()
        stats.discord_id = discord_id
        return stats

    def update(self, date, global_rank: int, country_rank: int, score_rank: int, country_score_rank: int):
        stats = DBStats()
        for k,v in self.__dict__.items():
            if k.startswith("_"):
                continue
            setattr(stats, k, v)
        stats.date = date
        if global_rank > 0:
            stats.global_rank = global_rank
            stats.country_rank = country_rank
        if score_rank > 0:
            stats.global_score_rank = score_rank
            stats.country_score_rank = country_score_rank
        return stats

class DBStatsCompact(Base):

    __tablename__ = 'live_leaderboard'
    
    id = Column('user_id', Integer, primary_key=True)
    server = Column('server', String, primary_key=True)
    leaderboard_type = Column('leaderboard_type', String, primary_key=True)
    mode = Column('mode', SmallInteger, primary_key=True)
    relax = Column('relax', SmallInteger, primary_key=True)
    global_rank = Column('global_rank', Integer)
    country_rank = Column('country_rank', Integer)
    score = Column('score', Float) # Depends on leaderboard type
    pp = Column('pp', Float)
    ranked_score = Column('ranked_score', BigInteger)
    total_score = Column('total_score', BigInteger)
    play_count = Column('play_count', Integer)
    replays_watched = Column('replays_watched', Integer)
    total_hits = Column('total_hits', Integer)
    accuracy = Column('accuracy', Float)
    
    
class DBScore(Base):
    
    __tablename__ = 'scores'
    
    id = Column('id', BigInteger, primary_key=True)
    user_id = Column('user_id', Integer)
    server = Column('server', String, primary_key=True)
    beatmap_id = Column('beatmap_id', Integer, ForeignKey('beatmaps.id'))
    beatmap_md5 = Column('beatmap_md5', String)
    max_combo = Column('max_combo', Integer)
    full_combo = Column('full_combo', Boolean)
    count_300 = Column('count_300', Integer)
    count_100 = Column('count_100', Integer)
    count_50 = Column('count_50', Integer)
    count_miss = Column('count_miss', Integer)
    count_katu = Column('count_katu', Integer)
    count_geki = Column('count_geki', Integer)
    accuracy = Column('accuracy', Float)
    rank = Column('rank', String)
    pp = Column('pp', Float)
    score = Column('score', Integer)
    mods = Column('mods', Integer)
    mods_lazer = Column('mods_lazer', JSONB)
    mode = Column('mode', SmallInteger)
    relax = Column('relax', SmallInteger)
    completed = Column('completed', SmallInteger)
    pinned = Column('pinned', Boolean)
    date = Column('date', DateTime)
    
    hidden = Column('hidden', Boolean)
    pp_system = Column('pp_system', String)
    last_updated = Column('last_updated', DateTime)
    extra_metadata = Column('extra_metadata', JSONB)
    beatmap = relationship('DBBeatmap', backref='user_scores', lazy='selectin', join_depth=2)
    
    def get_total_hits(self):
        return self.count_300 + self.count_100 + self.count_50 + self.count_miss

class DBFirstPlace(Base):
    
    __tablename__ = 'first_places'
    
    id = Column('score_id', Integer, primary_key=True)
    user_id = Column('user_id', Integer)
    server = Column('server', String, primary_key=True)
    mode = Column('mode', SmallInteger, primary_key=True)
    relax = Column('relax', SmallInteger, primary_key=True)
    beatmap_id = Column('beatmap_id', Integer)
    date = Column('date', Date, primary_key=True)


class DBClan(Base):
    
    __tablename__ = 'clans'

    id = Column('clan_id', Integer, primary_key=True)
    server = Column('server', String, primary_key=True)
    owner = Column('owner_id', Integer)
    name = Column('name', String)
    tag = Column('tag', String)
    description = Column('description', String)
    icon = Column('icon', String)
    status = Column('status', Integer)

class DBClanStats(Base):
    
    __tablename__ = 'clan_stats'
    
    id = Column('clan_id', Integer, primary_key=True)
    server = Column('server', String, primary_key=True)
    mode = Column('mode', SmallInteger, primary_key=True)
    relax = Column('relax', SmallInteger, primary_key=True)
    ranked_score = Column('ranked_score', BigInteger)
    total_score = Column('total_score', BigInteger)
    play_count = Column('play_count', Integer)
    replays_watched = Column('replays_watched', Integer)
    total_hits = Column('total_hits', Integer)
    accuracy = Column('accuracy', Float)
    pp = Column('pp', Float)
    first_places = Column('first_places', Integer)
    rank_pp = Column('rank_pp', Integer)
    rank_1s = Column('rank_1s', Integer)

class DBClanStatsCompact(Base):
    
    __tablename__ = 'live_clan_leaderboard'
    
    id = Column('clan_id', Integer, primary_key=True)
    server = Column('server', String, primary_key=True)
    mode = Column('mode', SmallInteger, primary_key=True)
    relax = Column('relax', SmallInteger, primary_key=True)
    ranked_score = Column('ranked_score', BigInteger)
    total_score = Column('total_score', BigInteger)
    play_count = Column('play_count', Integer)
    accuracy = Column('accuracy', Float)
    pp = Column('pp', Float)
    first_places = Column('first_places', Integer)
    rank_pp = Column('rank_pp', Integer)
    rank_1s = Column('rank_1s', Integer)

class DBMapPlaycount(Base):
    
    __tablename__ = 'user_most_played'
    
    user_id = Column('user_id', Integer, primary_key=True)
    server = Column('server', String, primary_key=True)
    beatmap_id = Column('beatmap_id', Integer, primary_key=True)
    play_count = Column('play_count', Integer)

class DBUserQueue(Base):
    
    __tablename__ = 'queue'
    
    user_id = Column('user_id', Integer, primary_key=True)
    server = Column('server', String, primary_key=True)
    mode = Column('mode', SmallInteger, primary_key=True)
    relax = Column('relax', SmallInteger, primary_key=True)
    date = Column('date', Date, primary_key=True)

class DBBeatmapPack(Base):
    
    __tablename__ = "beatmap_packs"
    
    author = Column('author', String)
    date = Column('date', DateTime)
    name = Column('name', String)
    link = Column('download_link', String)
    tag = Column('tag', String, primary_key=True)
    no_diff_reduction = Column('no_diff_reduction', Boolean)
    beatmapsets = Column('beatmapsets_id', ARRAY(Integer))

class DBAkatsukiPlaytime(Base):
    
    __tablename__ = "akatsuki_playtime"
    
    user_id = Column('user_id', Integer, primary_key=True)
    mode = Column('mode', SmallInteger, primary_key=True)
    relax = Column('relax', SmallInteger, primary_key=True)
    playtime = Column('playtime', Integer)

class DBBotLink(Base):
    
    __tablename__ = "bot_links"
    
    discord_id = Column('discord_id', BigInteger, primary_key=True)
    permissions = Column('permissions', SmallInteger)
    default_server = Column('default_server', String)
    default_mode = Column('default_mode', SmallInteger)
    default_relax = Column('default_relax', SmallInteger)
    links = Column('servers', JSONB)
    preferences = Column('preferences', JSONB)

class DBServerPreferences(Base):
    
    __tablename__ = "server_preferences"
    
    guild_id = Column('guild_id', BigInteger, primary_key=True)
    prefix = Column('prefix', String)
