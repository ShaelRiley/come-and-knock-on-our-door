#!/usr/bin/env python3
"""Original SCI1.1 audio fixtures. Standard library only; no game templates.

The SMF sources below are newly authored diagnostic notes, not an adaptation of
the supplied production score. Native output is statically checked, not claimed
audibly correct until an unchanged ScummVM integration has been captured.
"""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
import struct
import wave

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "generated"
PPQ = 480
SCI_TICK_US = 16667
LOOP_START = 6
BAR_TICKS = 120
BARS = 8
LOOP_END = LOOP_START + BARS * BAR_TICKS
GUARD = 3


def vlq(value: int) -> bytes:
    if not 0 <= value < 1 << 28:
        raise ValueError("SMF VLQ out of range")
    out = [value & 127]
    while value >> 7:
        value >>= 7
        out.insert(0, 128 | (value & 127))
    return bytes(out)


def read_vlq(data: bytes, pos: int) -> tuple[int, int]:
    value = 0
    for _ in range(4):
        b = data[pos]
        pos += 1
        value = value * 128 + (b & 127)
        if b < 128:
            return value, pos
    raise ValueError("Overlong SMF VLQ")


def write_smf(events: list[tuple[int, int, bytes]], end: int) -> bytes:
    events = [(0, -20, b"\xff\x51\x03\x07\xa1\x20"),
              (0, -19, b"\xff\x58\x04\x04\x02\x18\x08")] + events
    events += [(end, 99, b"\xff\x2f\x00")]
    body = bytearray()
    last = 0
    for tick, _, msg in sorted(events, key=lambda e: (e[0], e[1])):
        body += vlq(tick - last) + msg
        last = tick
    return b"MThd" + struct.pack(">IHHH", 6, 0, 1, PPQ) + b"MTrk" + struct.pack(">I", len(body)) + body


def parse_smf(data: bytes) -> tuple[int, list[tuple[int, int, bytes]]]:
    if data[:4] != b"MThd":
        raise ValueError("Missing MThd")
    size, fmt, tracks, ppq = struct.unpack_from(">IHHH", data, 4)
    if size != 6 or fmt not in (0, 1) or ppq & 0x8000 or not ppq:
        raise ValueError("Only PPQ SMF format 0/1 is supported")
    result = []
    pos = 14
    serial = 0
    for _ in range(tracks):
        if data[pos:pos + 4] != b"MTrk":
            raise ValueError("Missing MTrk")
        length = struct.unpack_from(">I", data, pos + 4)[0]
        track_end = pos + 8 + length
        pos += 8
        tick = 0
        running = None
        while pos < track_end:
            delta, pos = read_vlq(data, pos)
            tick += delta
            status = data[pos]
            if status >= 128:
                pos += 1
                if status < 0xf0:
                    running = status
            elif running is not None:
                status = running
            else:
                raise ValueError("Missing running status")
            if status == 0xff:
                kind = data[pos]
                size, pos = read_vlq(data, pos + 1)
                payload = data[pos:pos + size]
                pos += size
                message = bytes((status, kind)) + payload
            elif 0x80 <= status < 0xf0:
                size = 1 if status & 0xf0 in (0xc0, 0xd0) else 2
                payload = data[pos:pos + size]
                pos += size
                if len(payload) != size or any(b >= 128 for b in payload):
                    raise ValueError("Invalid MIDI parameters")
                message = bytes((status,)) + payload
            else:
                raise ValueError("SysEx/system input is intentionally unsupported")
            result.append((tick, serial, message))
            serial += 1
        if pos != track_end:
            raise ValueError("Invalid MTrk length")
    if pos != len(data):
        raise ValueError("Trailing SMF bytes")
    return ppq, sorted(result, key=lambda e: (e[0], e[1]))


def convert_smf(data: bytes) -> tuple[list[tuple[int, bytes]], list[dict]]:
    """Integrate source tempo exactly, then round ABSOLUTE time, never deltas."""
    ppq, events = parse_smf(data)
    tempo = 500000
    last_source_tick = 0
    elapsed = Fraction(0)
    converted, timing = [], []
    for source_tick, _, message in events:
        elapsed += Fraction((source_tick - last_source_tick) * tempo, ppq)
        last_source_tick = source_tick
        scaled = elapsed / SCI_TICK_US
        target = (scaled.numerator * 2 + scaled.denominator) // (2 * scaled.denominator)
        error = abs(Fraction(target * SCI_TICK_US) - elapsed)
        if error > Fraction(SCI_TICK_US, 2):
            raise AssertionError("Absolute quantization exceeded half a tick")
        if message[:2] == b"\xff\x51":
            if len(message) != 5:
                raise ValueError("Invalid tempo event")
            tempo = int.from_bytes(message[2:], "big")
            if tempo <= 0:
                raise ValueError("Invalid tempo")
        elif message[0] < 0xf0:
            if message[0] & 15 == 15:
                raise ValueError("Channel 15 reserved for generated SCI controls")
            converted.append((target, message))
            timing.append({"source_tick": source_tick, "source_us": float(elapsed),
                           "sci_tick": target, "error_us": float(error), "message": message.hex()})
    return converted, timing


def delta(value: int) -> bytes:
    if value < 0:
        raise ValueError("Negative SCI delta")
    return b"\xf8" * (value // 240) + bytes((value % 240,))


def sound_resource(channels: dict[int, list[tuple[int, bytes]]], voices: dict[int, int]) -> bytes:
    """SCI track 07, six-byte descriptors, explicit-status channel streams."""
    # Control first fixes tie order and makes its loop marker deterministic.
    order = sorted(channels, key=lambda c: (c != 15, c))
    header_size = 3 + 6 * len(order)
    payloads = []
    for channel in order:
        raw = bytearray((channel | (0x20 if channel == 9 else 0), voices.get(channel, 0)))
        last = 0
        for tick, msg in sorted(channels[channel], key=lambda e: e[0]):
            if msg[0] & 15 != channel or not 0x80 <= msg[0] < 0xf0:
                raise ValueError("Wrong channel or unsupported native message")
            raw += delta(tick - last) + msg
            last = tick
        raw += b"\x00\xfc"  # No omitted terminal delay in SCI channel mixing.
        payloads.append(bytes(raw))
    header = bytearray((7,))
    offset = header_size
    for payload in payloads:
        if offset + len(payload) >= 65536:
            raise ValueError("Conservative 64 KiB resource limit exceeded")
        header += struct.pack("<HHH", 0, offset, len(payload))
        offset += len(payload)
    return bytes(header) + b"\xff\xff" + b"".join(payloads)


def decode_sound(payload: bytes) -> dict[int, list[tuple[int, bytes]]]:
    """Independent strict reader used by tests and manifest validation."""
    if payload[0] != 7:
        raise ValueError("Expected a native GM track")
    descriptors = []
    pos = 1
    while payload[pos] != 255:
        unused, offset, size = struct.unpack_from("<HHH", payload, pos)
        if unused or offset + size > len(payload) or size < 4:
            raise ValueError("Bad descriptor")
        descriptors.append((offset, size))
        pos += 6
    if payload[pos:pos + 2] != b"\xff\xff":
        raise ValueError("Missing resource terminator")
    next_offset = pos + 2
    decoded = {}
    for offset, size in descriptors:
        if offset != next_offset:
            raise ValueError("Noncontiguous channel data")
        end = offset + size
        next_offset = end
        channel = payload[offset] & 15
        if channel in decoded:
            raise ValueError("Duplicate channel")
        pos = offset + 2
        tick = 0
        events = []
        while pos < end:
            duration = 0
            while payload[pos] == 248:
                duration += 240
                pos += 1
            duration += payload[pos]
            pos += 1
            tick += duration
            status = payload[pos]
            pos += 1
            if status == 252:
                if duration or pos != end:
                    raise ValueError("Terminal FC must be zero-delta and final")
                break
            if not 0x80 <= status < 0xf0 or status & 15 != channel:
                raise ValueError("Bad native status")
            length = 1 if status & 0xf0 in (0xc0, 0xd0) else 2
            params = payload[pos:pos + length]
            pos += length
            if len(params) != length or any(v >= 128 for v in params):
                raise ValueError("Bad native MIDI parameters")
            events.append((tick, bytes((status,)) + params))
        else:
            raise ValueError("Missing FC")
        decoded[channel] = events
    if next_offset != len(payload):
        raise ValueError("Trailing channel bytes")
    return decoded


def gm_patch() -> bytes:
    identity = bytes(range(128))
    return identity + bytes(256) + identity + b"\0" + bytes(128) + identity * 4 + b"\0\0"


def source_bed() -> bytes:
    events = []
    def add(tick, msg, priority=1):
        events.append((tick * 16, priority, bytes(msg)))
    def note(tick, length, channel, pitch, velocity):
        add(tick, [0x90 | channel, pitch, velocity], 2)
        add(tick + length, [0x80 | channel, pitch, 0], 0)
    for channel, program, volume, pan in [(0, 32, 80, 64), (1, 0, 55, 55),
                                           (2, 71, 0, 40), (3, 73, 0, 88)]:
        add(0, [0xc0 | channel, program])
        add(0, [0xb0 | channel, 7, volume])
        add(0, [0xb0 | channel, 10, pan])
        add(0, [0xb0 | channel, 64, 0])
        add(0, [0xe0 | channel, 0, 64])
    roots = [48, 48, 53, 55, 48, 57, 53, 55]
    motif = [72, 76, 74, 79, 77, 76, 69, 72]
    for bar, root in enumerate(roots):
        start = LOOP_START + bar * BAR_TICKS
        for beat in range(4):
            t = start + beat * 30
            note(t, 21, 0, root - 12 + (7 if beat & 1 else 0), 63)
            for interval in (0, 3 if root == 57 else 4, 7):
                note(t + 15, 9, 1, root + interval, 45)
            note(t, 21, 2, motif[(bar + beat) % 8], 66)
            note(t + 15, 9, 3, motif[(bar + beat + 2) % 8] - 12, 72)
    return write_smf(events, LOOP_END * 16)


def source_stinger() -> bytes:
    events = [(0, 0, bytes((0xc4, 9))), (0, 0, bytes((0xb4, 7, 90))),
              (0, 0, bytes((0xb4, 10, 64))), (0, 0, bytes((0xb4, 64, 0)))]
    for index, pitch in enumerate((72, 76, 79, 84)):
        start = 6 + index * 10
        events += [(start * 16, 2, bytes((0x94, pitch, 72))),
                   ((start + (18 if index == 3 else 8)) * 16, 0, bytes((0x84, pitch, 0)))]
    return write_smf(events, 60 * 16)


def native_from_smf(smf: bytes, bed: bool) -> tuple[bytes, list[dict]]:
    midi, timing = convert_smf(smf)
    channels = {}
    for tick, msg in midi:
        channels.setdefault(msg[0] & 15, []).append((tick, msg))
    if bed:
        # Prefix gives getSongReverb its expected byte at control-data offset 6.
        controls = [(0, b"\xcf\x00"), (0, b"\xbf\x50\x00")]
        for bar in range(BARS + 1):
            boundary = LOOP_START + bar * BAR_TICKS
            controls.append((boundary - GUARD, bytes((0xcf, bar % BARS + 1))))
        # Reverb event at identical time updates parser playTick before CF127.
        controls += [(LOOP_START, b"\xbf\x50\x00"), (LOOP_START, b"\xcf\x7f"),
                     (LOOP_END, b"\xbf\x50\x00")]
    else:
        controls = [(0, b"\xcf\x00"), (0, b"\xbf\x50\x00"), (60, b"\xbf\x50\x00")]
    channels[15] = sorted(controls, key=lambda e: e[0])
    payload = sound_resource(channels, {0: 1, 1: 3, 2: 1, 3: 1, 4: 1, 15: 0})
    return payload, timing


def validate(payload: bytes, bed: bool) -> dict:
    channels = decode_sound(payload)
    maximum_end = 0
    for channel, events in channels.items():
        active = set()
        for tick, msg in events:
            maximum_end = max(tick, maximum_end)
            command = msg[0] & 0xf0
            if command == 0x90 and msg[2]:
                if msg[1] in active:
                    raise AssertionError("Overlapping same-pitch note")
                active.add(msg[1])
            elif command == 0x80 or (command == 0x90 and not msg[2]):
                if msg[1] not in active:
                    raise AssertionError("Unmatched note off")
                active.remove(msg[1])
        if active:
            raise AssertionError("Hanging final note")
    if bed:
        assert maximum_end == LOOP_END
        assert {ch for ch in channels if ch != 15} == {0, 1, 2, 3}
        for channel in (2, 3):
            active = set()
            index = 0
            events = channels[channel]
            for tick in range(LOOP_END + 1):
                while index < len(events) and events[index][0] == tick:
                    msg = events[index][1]
                    if msg[0] & 0xf0 == 0x90 and msg[2]:
                        active.add(msg[1])
                    elif msg[0] & 0xf0 == 0x80:
                        active.discard(msg[1])
                    index += 1
                if any(b - GUARD <= tick < b for b in range(LOOP_START, LOOP_END + 1, BAR_TICKS)):
                    assert not active, ("Non-silent guard", channel, tick)
            assert all(t == 0 for t, m in events if m[:2] == bytes((0xb0 | channel, 7)))
        cues = [(t, m[1]) for t, m in channels[15] if m[0] == 0xcf and 1 <= m[1] <= 8]
        assert cues == [(LOOP_START + b * BAR_TICKS - GUARD, b % BARS + 1) for b in range(9)]
        assert (LOOP_START, b"\xcf\x7f") in channels[15]
    else:
        assert maximum_end == 60
        assert set(channels) == {4, 15}
    return {"channels_zero_based": sorted(channels), "event_count": sum(map(len, channels.values())),
            "last_tick": maximum_end, "all_notes_balanced": True,
            "three_tick_note_silent_guards": bed, "native_runtime_capture": "pending"}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build(output: Path = OUT) -> dict:
    for sub in ("source", "payloads", "patches"):
        (output / sub).mkdir(parents=True, exist_ok=True)
    resources, written = [], {}
    def emit(name: str, data: bytes):
        (output / name).write_bytes(data)
        written[name] = {"bytes": len(data), "sha256": sha(data)}
    for number, name, smf, bed in [(1, "bed", source_bed(), True), (2, "stinger", source_stinger(), False)]:
        payload, timing = native_from_smf(smf, bed)
        report = validate(payload, bed)
        emit(f"source/{name}.mid", smf)
        emit(f"payloads/{number:03d}.sound.bin", payload)
        emit(f"patches/sound.{number:03d}", b"\x84\x00" + payload)
        emit(f"source/{name}-timing.json", (json.dumps(timing, indent=2) + "\n").encode())
        resources.append({"type": "sound", "id": number, "role": name,
                          "payload": f"payloads/{number:03d}.sound.bin", "validation": report,
                          "maximum_absolute_quantization_error_us": max(t["error_us"] for t in timing)})
    patch = gm_patch()
    assert len(patch) == 1155 and int.from_bytes(patch[1153:], "little") == 0
    emit("payloads/004.patch.bin", patch)
    emit("patches/patch.004", b"\x89\x00" + patch)
    pcm_path = ROOT / "assets/proof/audience_lane_test.wav"
    pcm = pcm_path.read_bytes()
    with wave.open(str(pcm_path), "rb") as stream:
        pcm_info = {"channels": stream.getnchannels(), "sample_width_bytes": stream.getsampwidth(),
                    "sample_rate": stream.getframerate(), "frames": stream.getnframes()}
    assert pcm_info["channels"] == 1 and pcm_info["sample_width_bytes"] == 2
    emit("patches/@0010101.001", pcm)
    manifest = {"status": "static resource proof only; native integration and captured timing pending",
                "provenance": "New original diagnostic notes; existing original synthetic proof-chuff reused byte-for-byte. No commercial game resources or template code.",
                "engine_target": "unmodified ScummVM v2026.3.0 SCI1.1 + FluidSynth + FluidR3",
                "timing": {"source_ppq": PPQ, "source_tempo_us_per_quarter": 500000,
                           "resource_tick_us": SCI_TICK_US, "loop_start_tick": LOOP_START,
                           "loop_end_tick": LOOP_END, "ticks_per_bar": BAR_TICKS,
                           "guard_ticks": GUARD, "loop_bars": BARS,
                           "cue_values": "1..8 at three ticks before the upcoming bar; 1 repeats before loop wrap",
                           "guard_scope": "No held MIDI notes in changing channels; acoustic release/reverb and actual scheduling require capture."},
                "mixes": {"A": {"channel_2": 85, "channel_3": 0}, "B": {"channel_2": 0, "channel_3": 85},
                          "base_only": {"channel_2": 0, "channel_3": 0}},
                "resources": resources + [{"type": "patch", "id": 4, "role": "identity GM mapping", "payload": "payloads/004.patch.bin"}],
                "audience": {"patch": "patches/@0010101.001", "tuple": [1, 1, 1, 0, 1],
                             "source": "assets/proof/audience_lane_test.wav", "source_sha256": sha(pcm),
                             "pcm": pcm_info, "speech_category": True, "simultaneous_pcm_policy": "one player; replace or skip", "human_laugh_recording": False},
                "files": written}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    result = build()
    print(json.dumps({"output": str(OUT), "status": result["status"], "resources": result["resources"]}, indent=2))
