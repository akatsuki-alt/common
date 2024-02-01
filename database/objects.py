from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from datetime import datetime
from typing import Optional

from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy import *


Base = declarative_base()

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
