### `wrpl_parser_ng.py`

This module is responsible for parsing and unpacking client replay files. It uses the `construct` library to define the structure of the replay file and extract relevant information.

#### Imports
- `enum`: Provides support for enumerations.
- `typing as t`: Provides type hints.
- `construct as ct`: The `construct` library for defining and parsing binary data structures.
- `this`: A special object in `construct` for referencing the current context.
- `blk.binary as bin`: Custom module for handling binary data.

#### Functions

- **`no_encoder(obj, context)`**:
  - Raises `NotImplementedError`.
  - Used as a placeholder for encoding functions that are not implemented.

- **`StringField(sz: t.Union[int, callable]) -> ct.Construct`**:
  - Returns a `construct` object for a fixed-size ASCII string field.
  - Parameters:
    - `sz`: Size of the string field.

#### Enums

- **`Difficulty(enum.IntEnum)`**:
  - Represents different difficulty levels.
  - Values:
    - `ARCADE = 0b0000`
    - `REALISTIC = 0b0101`
    - `HARDCORE = 0b1010`

- **`SessionType(enum.IntEnum)`**:
  - Represents different session types.
  - Values:
    - `AIR_SIM = 0x3C`
    - `MARINE_BATTLE = 0x1a`
    - `RANDOM_BATTLE = 0x20`
    - `CUSTOM_BATTLE = 0x40`
    - `USER_MISSION = 0x01`

#### Constructs

- **`DifficultyCon`**:
  - A `construct` adapter for the `Difficulty` enum.
  - Uses bitwise operations to extract the difficulty value.

- **`Header`**:
  - Defines the structure of the replay file header.
  - Fields:
    - `magic`: Constant value `0xe5ac0010`.
    - `version`: 32-bit unsigned integer.
    - `level`: Fixed-size ASCII string (128 bytes).
    - `level_settings`: Fixed-size ASCII string (260 bytes).
    - `battle_type`: Fixed-size ASCII string (128 bytes).
    - `environment`: Fixed-size ASCII string (128 bytes).
    - `visibility`: Fixed-size ASCII string (32 bytes).
    - `rez_offset`: 32-bit unsigned integer.
    - `difficulty`: `DifficultyCon` construct.
    - `unk_35`: 35 bytes.
    - `session_type`: Byte.
    - `unk_3`: 3 bytes.
    - `session_id`: 64-bit unsigned integer.
    - `unk_8`: 8 bytes.
    - `m_set_size`: 32-bit unsigned integer.
    - `unk_32`: 32 bytes.
    - `loc_name`: Fixed-size ASCII string (128 bytes).
    - `start_time`: 32-bit unsigned integer.
    - `time_limit`: 32-bit unsigned integer.
    - `score_limit`: 32-bit unsigned integer.
    - `unk_48`: 48 bytes.
    - `battle_class`: Fixed-size ASCII string (128 bytes).
    - `battle_kill_streak`: Fixed-size ASCII string (128 bytes).

- **`FatBlockStream(sz: t.Union[int, callable, None] = None) -> ct.Construct`**:
  - Returns a `construct` object for a FAT block stream.
  - Parameters:
    - `sz`: Size of the stream.

- **`ZlibStream(sz: t.Union[int, callable, None] = None)`**:
  - Returns a `construct` object for a zlib-compressed stream.
  - Parameters:
    - `sz`: Size of the stream.

- **`WRPLCliFile`**:
  - Defines the structure of the replay file.
  - Fields:
    - `header`: `Header` construct.
    - `m_set`: FAT block stream.
    - `rez_offset`: Current file position.
    - `rez`: FAT block.