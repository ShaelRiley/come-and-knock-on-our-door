"""Portable original-project bitmap/font/palette encoders. Adapted 2026-10-08."""
import struct
def u16(value: int) -> bytes:
    return struct.pack("<H", value)

def font_resource(glyphs: dict) -> bytes:
    count = 128
    payload = bytearray(u16(0) + u16(count) + u16(8) + bytes(count * 2))
    for code in range(count):
        struct.pack_into("<H", payload, 6 + code * 2, len(payload))
        rows = glyphs.get(chr(code).upper(), glyphs["?"])
        if code < 32 or code == 127:
            rows = [0] * 7
        # SCI bitmap glyphs: width, height, then MSB-first packed scanlines.
        payload += bytes([6, 8] + [row << 3 for row in rows] + [0])
    return bytes(payload)

def palette_resource(colors: list) -> bytes:
    # SCI1.1 constant-color palette: 37-byte header, followed by RGB triples.
    palette = list(colors) + [(0, 0, 0)] * (256 - len(colors))
    header = bytearray(37)
    header[25] = 0
    struct.pack_into("<H", header, 29, 256)
    header[32] = 1
    return bytes(header) + bytes(component for color in palette for component in color)
