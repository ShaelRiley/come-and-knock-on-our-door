"""Independently authored SCI1.1 VGA view encoder, targeting stock ScummVM.

Only format fields are derived from ScummVM's public decoder. No upstream code,
commercial pixels, or template resource bytes are incorporated in the output.
This deliberately small subset has literal scanlines, no mirrors, no embedded
palette, no scaling metadata, and zero cel displacements.
"""
from __future__ import annotations

from dataclasses import dataclass
import struct
from typing import Sequence

HEADER_SIZE = 18
LOOP_SIZE = 16
CEL_SIZE = 36
RESOURCE_LIMIT = 65535
CLEAR_KEY = 255


@dataclass(frozen=True)
class Cel:
    width: int
    height: int
    pixels: bytes
    clear_key: int = CLEAR_KEY


def encode_view(loops: Sequence[Sequence[Cel]]) -> bytes:
    """Encode top-down, left-to-right palette indices as an SCI1.1 payload.

    The result has no patch-file prefix and no map/volume record header. Feed it
    to pack.pack_resources under resource type 0. Each cel's literal pointer is
    absolute from payload byte zero; RLE pointer zero selects uncompressed data.
    """
    if not 1 <= len(loops) <= 255:
        raise ValueError("A view needs 1..255 non-mirrored loops")
    flat = []
    for loop in loops:
        if not 1 <= len(loop) <= 255:
            raise ValueError("Each loop needs 1..255 cels")
        for cel in loop:
            if not 1 <= cel.width <= 32767 or not 1 <= cel.height <= 32767:
                raise ValueError("Cel dimensions must be positive signed 16-bit values")
            if not isinstance(cel.pixels, bytes):
                raise ValueError("Cel pixels must be immutable palette-index bytes")
            if len(cel.pixels) != cel.width * cel.height:
                raise ValueError("Cel byte count does not match its dimensions")
            if not 0 <= cel.clear_key <= 255:
                raise ValueError("Clear key must be a palette index")
            flat.append(cel)
    data_start = HEADER_SIZE + LOOP_SIZE * len(loops) + CEL_SIZE * len(flat)
    size = data_start + sum(len(c.pixels) for c in flat)
    if size > RESOURCE_LIMIT:
        raise ValueError(f"View payload {size} exceeds the SCI16 65535-byte limit")

    out = bytearray(size)
    # HeaderSize excludes its own word; byte 4 is the SCI1.1 format marker.
    struct.pack_into("<HBBHHIBBHH", out, 0,
                     HEADER_SIZE - 2, len(loops), 0, 1, len(flat), 0,
                     LOOP_SIZE, CEL_SIZE, 320, 200)
    cel_index = 0
    data_offset = data_start
    for loop_index, loop in enumerate(loops):
        loop_offset = HEADER_SIZE + loop_index * LOOP_SIZE
        cel_offset = HEADER_SIZE + len(loops) * LOOP_SIZE + cel_index * CEL_SIZE
        # 255 means this loop owns its cels and is not a mirror of another loop.
        struct.pack_into("<BBBBIII", out, loop_offset,
                         255, 0, len(loop), 0, 0, 0, cel_offset)
        for cel in loop:
            # Width, height, x/y displacement, clear key, encoding, reserved.
            struct.pack_into("<hhhhBBH", out, cel_offset,
                             cel.width, cel.height, 0, 0, cel.clear_key, 0, 0)
            # Pixel byte count, RLE byte count, palette offset, RLE pointer,
            # literal pointer, row-table pointer. No compressed/row-table data.
            struct.pack_into("<IIIIII", out, cel_offset + 12,
                             len(cel.pixels), 0, 0, 0, data_offset, 0)
            out[data_offset:data_offset + len(cel.pixels)] = cel.pixels
            data_offset += len(cel.pixels)
            cel_offset += CEL_SIZE
            cel_index += 1
    return bytes(out)
