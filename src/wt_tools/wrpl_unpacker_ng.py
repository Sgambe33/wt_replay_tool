"""
Unpacking client replay.

Input:
#2021.09.20 19.30.33.wrpl

Output:
#2021.09.20 19.30.33.wrpl.d/
├── m_set.blkx
├── rez.blkx
├── info.json
└── wrplu.bin
"""
import json
import typing as t
import os
import sys

import blk.json
import construct as ct

from blk import Format
from blk.types import Section
import blk.text as txt
import blk.json as jsn

try:
    from formats.wrpl_parser_ng import WRPLCliFile
except ImportError:
    from wt_tools.formats.wrpl_parser_ng import WRPLCliFile

STRICT_BLK = 'strict_blk'
JSON = 'json'
JSON_2 = 'json_2'
JSON_3 = 'json_3'

out_type_map = {
    STRICT_BLK: blk.Format.STRICT_BLK,
    JSON: blk.Format.JSON,
    JSON_2: blk.Format.JSON_2,
    JSON_3: blk.Format.JSON_3,
}


def suffix(out_format: str) -> str:
    return '.blkx' if out_format == STRICT_BLK else '.json'


def serialize_text(root: Section, out_type: Format, is_sorted: bool = False) -> str:
    """Serializes a Section object to a text string."""
    if out_type == blk.Format.STRICT_BLK:
        from io import StringIO
        ostream = StringIO()
        txt.serialize(root, ostream, dialect=txt.StrictDialect)
        return ostream.getvalue()
    elif out_type in (blk.Format.JSON, blk.Format.JSON_2, blk.Format.JSON_3):
        return jsn.serialize(root, out_type, is_sorted)
    else:
        raise ValueError(f"Unsupported format: {out_type}")


def create_text(path: os.PathLike) -> t.TextIO:
    return open(path, 'w', newline='', encoding='utf8')


def parse_replay(replay_file: str, out_type: Format) -> dict:
    with open(replay_file, 'rb') as f:
        try:
            parsed = WRPLCliFile.parse_stream(f)
        except ct.ConstructError as e:
            print('Error parsing input file {}: {}'.format(f.name, e), file=sys.stderr)

    M_SET = json.loads(serialize_text(parsed['m_set'], out_type))
    REZ = json.loads(serialize_text(parsed['rez'], out_type))

    return {
        'm_set': M_SET,
        'rez': REZ,
        'info': {
            'version': parsed.header.version,
            'level': parsed.header.level,
            'level_settings': parsed.header.level_settings,
            'battle_type': parsed.header.battle_type,
            'environment': parsed.header.environment,
            'visibility': parsed.header.visibility,
            'difficulty': int(parsed.header.difficulty),
            'session_type': int(parsed.header.session_type),
            'session_id': parsed.header.session_id,
            'loc_name': parsed.header.loc_name,
            'battle_class': parsed.header.battle_class,
            'start_time': parsed.header.start_time,
            'time_limit': parsed.header.time_limit,
            'score_limit': parsed.header.score_limit,
            'battle_kill_streak': parsed.header.battle_kill_streak,
            'm_set_size': parsed.header.m_set_size,
            'rez_offset': parsed.header.rez_offset,
        }
    }
