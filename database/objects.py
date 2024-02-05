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
    followers = Column('followers', Integer)
    banned = Column('banned', Boolean)

class DBStats(Base):

    __tablename__ = 'stats'
    
    server = Column('server', String, primary_key=True)
    user_id = Column('user_id', Integer, primary_key=True)
    mode = Column('mode', SmallInteger, primary_key=True)
    relax = Column('relax', SmallInteger, primary_key=True)
    
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

    extra_metadata = Column('extra_metadata', JSONB)

class DBScore(Base):
    
    __tablename__ = 'scores'
    
    id = Column('id', Integer, primary_key=True)
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

class DBMapPlaycount(Base):
    
    __tablename__ = 'user_most_played'
    
    user_id = Column('user_id', Integer, primary_key=True)
    server = Column('server', String, primary_key=True)
    beatmap_id = Column('beatmap_id', Integer, primary_key=True)
    play_count = Column('play_count', Integer)
