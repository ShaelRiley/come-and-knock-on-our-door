"""Independent strict bounds checker/decoder for our exported SCI1.1 subset.

This is intentionally not a general decoder for arbitrary Sierra game resources.
It rejects noncanonical fields, overlap, pointers into headers and trailing data.
No writer implementation or writer constants are imported here.
"""
from __future__ import annotations

import struct


class ViewFormatError(ValueError):
    pass


def decode_view(data: bytes) -> list[list[dict]]:
    def require(condition: bool, message: str) -> None:
        if not condition:
            raise ViewFormatError(message)

    def unpack(fmt: str, offset: int) -> tuple:
        require(0 <= offset and offset + struct.calcsize(fmt) <= len(data),
                f"Truncated field at {offset}")
        return struct.unpack_from(fmt, data, offset)

    require(18 <= len(data) <= 65535, "Invalid SCI16 view payload length")
    header, count, flags, version, total, palette, loop_size, cel_size, nx, ny = unpack(
        "<HBBHHIBBHH", 0)
    require(header == 16, "Header must occupy 18 bytes including its size word")
    require(1 <= count <= 255, "View needs at least one loop")
    require(flags == 0 and version == 1, "Unsupported flags or format marker")
    require(palette == 0, "Embedded palettes are outside the exported subset")
    require((loop_size, cel_size) == (16, 36), "Unexpected record stride")
    require((nx, ny) == (320, 200), "Unexpected native resolution metadata")
    first_cel = 18 + count * 16
    first_pixel = first_cel + total * 36
    require(first_pixel <= len(data), "Header tables exceed payload")
    next_cel, next_pixel, seen = first_cel, first_pixel, 0
    loops = []
    for loop_number in range(count):
        mirror, mirror_flag, cels, reserved, unused1, unused2, pointer = unpack(
            "<BBBBIII", 18 + loop_number * 16)
        require(mirror == 255 and mirror_flag == 0, "Mirrors are unsupported")
        require(cels > 0, "Empty loop")
        require((reserved, unused1, unused2) == (0, 0, 0), "Nonzero loop reserved fields")
        require(pointer == next_cel, "Cel table gap, overlap, or invalid pointer")
        loop = []
        for cel_number in range(cels):
            width, height, dx, dy, clear, encoding, unused = unpack("<hhhhBBH", next_cel)
            size, rle_size, pal, rle, literal, rows = unpack("<IIIIII", next_cel + 12)
            require(width > 0 and height > 0, "Invalid signed cel dimensions")
            require((dx, dy) == (0, 0), "Displacements must be zero")
            require((encoding, unused, rle_size, pal, rle, rows) == (0, 0, 0, 0, 0, 0),
                    "Only literal non-paletted cels are supported")
            require(size == width * height, "Pixel byte count mismatch")
            require(literal == next_pixel, "Pixel gap, overlap, or invalid pointer")
            require(literal + size <= len(data), "Truncated cel pixels")
            pixels = data[literal:literal + size]
            loop.append({"width": width, "height": height, "clear_key": clear,
                         "pixels": pixels, "header_offset": next_cel,
                         "literal_offset": literal,
                         "transparent_pixels": pixels.count(clear)})
            next_cel += 36
            next_pixel += size
            seen += 1
        loops.append(loop)
    require(seen == total, "Total cel count mismatch")
    require(next_cel == first_pixel, "Cel headers overlap pixels")
    require(next_pixel == len(data), "Trailing bytes")
    return loops
