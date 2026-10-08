#!/usr/bin/env python3
"""Original, uncompressed SCI1.1 resource writer and compiler-table seeder.

Implements the on-disk interface described by ScummVM's resource.cpp, kernel.cpp
and scifont.cpp. Does not import or copy Sierra/template game resources.
The font and palette are read as data from this project's original asset source.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TYPES = {"view": 0, "pic": 1, "script": 2, "text": 3, "sound": 4,
         "vocab": 6, "font": 7, "patch": 9, "palette": 11, "heap": 17}
SELECTORS = {
    "name": 0, "play": 1, "nodePtr": 2,
    "type": 3, "message": 4, "modifiers": 5, "x": 6, "y": 7,
    "-objID-": 0x1000, "-size-": 0x1001, "-propDict-": 0x1002,
    "-methDict-": 0x1003, "-classScript-": 0x1004, "-script-": 0x1005,
    "-super-": 0x1006, "-info-": 0x1007,
}


def u16(value: int) -> bytes:
    return struct.pack("<H", value)


def original_asset_data() -> tuple[dict, list]:
    """Read only literal assignments; never run the asset-generation program."""
    path = ROOT / "tools" / "generate_proof_assets.py"
    found = {}
    for node in ast.parse(path.read_text()).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in {"GLYPHS", "PALETTE"}:
                    # The space glyph is the sole simple multiplication expression.
                    value = node.value
                    if target.id == "GLYPHS":
                        for k, v in zip(value.keys, value.values):
                            if isinstance(v, ast.BinOp) and isinstance(v.op, ast.Mult):
                                assert ast.literal_eval(v.left) == [0] and ast.literal_eval(v.right) == 7
                                replacement = ast.List(elts=[ast.Constant(0)] * 7, ctx=ast.Load())
                                value.values[value.keys.index(k)] = replacement
                    found[target.id] = ast.literal_eval(value)
    return found["GLYPHS"], found["PALETTE"]


def selector_resource() -> bytes:
    count = max(SELECTORS.values()) + 1
    payload = bytearray(u16(count - 1) + bytes(count * 2))
    offsets = {}
    by_id = {value: name for name, value in SELECTORS.items()}
    for index in range(count):
        name = by_id.get(index, "BAD SELECTOR")
        if name not in offsets:
            offsets[name] = len(payload)
            encoded = name.encode("ascii")
            payload += u16(len(encoded)) + encoded
        struct.pack_into("<H", payload, 2 + index * 2, offsets[name])
    assert len(payload) < 65536
    return bytes(payload)


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


def pack_resources(resources: dict[tuple[int, int], bytes], out: Path) -> dict:
    """Write a SCI1.1 map/volume pair, including word-aligned volume records."""
    out.mkdir(parents=True, exist_ok=True)
    volume = bytearray()
    groups: dict[int, list[tuple[int, int]]] = {}
    records = []
    for (kind, number), payload in sorted(resources.items()):
        if len(volume) & 1:
            volume.append(0)
        offset = len(volume)
        if not 0 < len(payload) <= 65535:
            raise ValueError(f"Invalid SCI16 resource length: {kind}:{number} {len(payload)}")
        volume += struct.pack("<BHHHH", kind | 0x80, number, len(payload), len(payload), 0)
        volume += payload
        groups.setdefault(kind, []).append((number, offset))
        records.append({"type": kind, "number": number, "offset": offset,
                        "size": len(payload), "sha256": hashlib.sha256(payload).hexdigest()})
    # SCI1.1 volume records, including the last, use word alignment.
    if len(volume) & 1:
        volume.append(0)
    directory = bytearray()
    entries = bytearray()
    data_offset = (len(groups) + 1) * 3
    for kind, group in sorted(groups.items()):
        directory += bytes([kind | 0x80]) + u16(data_offset + len(entries))
        for number, offset in group:
            entries += u16(number) + (offset // 2).to_bytes(3, "little")
    directory += b"\xff" + u16(data_offset + len(entries))
    mapping = bytes(directory + entries)
    (out / "resource.map").write_bytes(mapping)
    (out / "resource.000").write_bytes(volume)
    manifest = {"format": "SCI1.1 uncompressed little-endian VGA", "resources": records,
                "files": {"resource.map": hashlib.sha256(mapping).hexdigest(),
                          "resource.000": hashlib.sha256(volume).hexdigest()}}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def base_resources() -> dict[tuple[int, int], bytes]:
    glyphs, colors = original_asset_data()
    return {(TYPES["vocab"], 996): bytes(4),
            (TYPES["vocab"], 997): selector_resource(),
            (TYPES["font"], 0): font_resource(glyphs),
            (TYPES["palette"], 999): palette_resource(colors)}


def validate_resources(out: Path) -> None:
    """Independent bounds/header/payload checks on a freshly generated package."""
    mapping = (out / "resource.map").read_bytes()
    volume = (out / "resource.000").read_bytes()
    dirs = []
    position = 0
    while True:
        kind, start = struct.unpack_from("<BH", mapping, position)
        position += 3
        dirs.append((kind, start))
        if kind == 255:
            break
    assert dirs[-1][1] == len(mapping)
    assert dirs[0][1] == position
    for (kind, start), (_, end) in zip(dirs, dirs[1:]):
        assert (end - start) % 5 == 0
        for pos in range(start, end, 5):
            number = struct.unpack_from("<H", mapping, pos)[0]
            offset = int.from_bytes(mapping[pos + 2:pos + 5], "little") * 2
            rkind, rnumber, packed, unpacked, compression = struct.unpack_from("<BHHHH", volume, offset)
            assert rkind == kind and rnumber == number
            assert packed == unpacked and compression == 0
            assert offset + 9 + packed <= len(volume)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["seed", "package", "check"])
    parser.add_argument("--out", type=Path)
    parser.add_argument("--script", type=Path, default=HERE / "build" / "compiled" / "0.scr.bin")
    args = parser.parse_args()
    out = args.out or (HERE if args.mode == "seed" else HERE / "build" / "game")
    if args.mode == "check":
        validate_resources(out)
        print(f"Validated {out}")
        return
    resources = base_resources()
    if args.mode == "package":
        resources[(TYPES["script"], 0)] = args.script.read_bytes()
        resources[(TYPES["heap"], 0)] = Path(str(args.script) + ".hep").read_bytes()
    pack_resources(resources, out)
    validate_resources(out)
    (HERE / "selectors.json").write_text(json.dumps(SELECTORS, indent=2, sort_keys=True) + "\n")
    print(f"Wrote and validated {len(resources)} original resources in {out}")


if __name__ == "__main__":
    main()
