# Credit osu alternative devs
from common.database.objects import DBBeatmap
from typing import List

import datetime
import struct
import gzip

OA_S_PER_DAY = 8.64e4
OA_EPOC = datetime.datetime(1899, 12, 30, 0, 0, 0, tzinfo=datetime.timezone.utc)


def OADoubleNow():
    return (
        datetime.datetime.now(datetime.timezone.utc) - OA_EPOC
    ).total_seconds() / OA_S_PER_DAY


def uleb128encode(n):
    assert n >= 0
    arr = []
    while True:
        b = n & 0x7F
        n >>= 7
        if n == 0:
            arr.append(b)
            return bytearray(arr)
        arr.append(0x80 | b)


def format_str(s):
    s = bytes(s, "utf-8")
    return uleb128encode(len(s)) + s


def generate_collection_from_db(beatmaps: List[DBBeatmap], collection_name):
    temp_bytes = format_str("o!dm8")
    temp_bytes += struct.pack("d", OADoubleNow())
    temp_bytes += format_str("N/A")
    temp_bytes += struct.pack("i", 1)

    temp_bytes += format_str(collection_name)
    temp_bytes += struct.pack("i", -1)  # online ID
    temp_bytes += struct.pack("i", len(beatmaps))  # amount of beatmaps

    for beatmap in beatmaps:
        temp_bytes += struct.pack("i", beatmap.id)
        temp_bytes += struct.pack("i", beatmap.set_id)
        temp_bytes += format_str(beatmap.beatmapset.artist)
        temp_bytes += format_str(beatmap.beatmapset.title)
        temp_bytes += format_str(beatmap.version)
        temp_bytes += format_str(beatmap.md5)
        temp_bytes += format_str("")
        temp_bytes += struct.pack("b", beatmap.mode)
        temp_bytes += struct.pack("d", beatmap.diff)

    temp_bytes += struct.pack("i", 0)
    temp_bytes += format_str("By Piotrekol")
        
    return format_str("o!dm8") + gzip.compress(temp_bytes)

def generate_collection_from_dict(beatmaps: List[dict], collection_name):
    temp_bytes = format_str("o!dm8")
    temp_bytes += struct.pack("d", OADoubleNow())
    temp_bytes += format_str("N/A")
    temp_bytes += struct.pack("i", 1)

    temp_bytes += format_str(collection_name)
    temp_bytes += struct.pack("i", -1)  # online ID
    temp_bytes += struct.pack("i", len(beatmaps))  # amount of beatmaps

    for beatmap in beatmaps:
        temp_bytes += struct.pack("i", beatmap['id'])
        temp_bytes += struct.pack("i", beatmap['set_id'])
        temp_bytes += format_str(beatmap['artist'])
        temp_bytes += format_str(beatmap['title'])
        temp_bytes += format_str(beatmap['version'])
        temp_bytes += format_str(beatmap['md5'])
        temp_bytes += format_str("")
        temp_bytes += struct.pack("b", beatmap['mode'])
        temp_bytes += struct.pack("d", beatmap['diff'])

    temp_bytes += struct.pack("i", 0)
    temp_bytes += format_str("By Piotrekol")
    
    return format_str("o!dm8") + gzip.compress(temp_bytes)