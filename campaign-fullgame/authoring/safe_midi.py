"""Original six-tick guard arrangement, portable adaptation 2026-10-08."""
import midi as g
START=12
END=972
GUARD=6
def make_safe():
    _, original = g.parse_smf(g.source_bed())
    events = []
    for source_tick, _, message in original:
        if message[0] >= 0xf0:
            continue
        kind, channel = message[0] & 0xf0, message[0] & 15
        priority = 0 if kind == 0x80 else (2 if kind == 0x90 else 1)
        # The last alternateB note used to end at bar+114. End it at111,
        # three ticks before the new six-tick guard begins at114.
        if kind == 0x80 and channel == 3 and (source_tick // 16 - g.LOOP_START) % 120 == 114:
            source_tick -= 3 * 16
        if source_tick:
            source_tick += 6 * 16
        events.append((source_tick, priority, message))
    source = g.write_smf(events, END * 16)
    midi, timing = g.convert_smf(source)
    channels = {}
    for tick, message in midi:
        channels.setdefault(message[0] & 15, []).append((tick, message))
    controls = [(0, b'\xcf\0'), (0, b'\xbf\x50\0')]
    controls += [(START + bar * 120 - GUARD, bytes((0xcf, bar % 8 + 1))) for bar in range(9)]
    controls += [(START, b'\xbf\x50\0'), (START, b'\xcf\x7f'), (END, b'\xbf\x50\0')]
    channels[15] = sorted(controls, key=lambda e: e[0])
    payload = g.sound_resource(channels, {0: 1, 1: 3, 2: 1, 3: 1, 15: 0})
    decoded = g.decode_sound(payload)
    for channel in (2, 3):
        active = set()
        stream = decoded[channel]
        index = 0
        for tick in range(END + 1):
            while index < len(stream) and stream[index][0] == tick:
                msg = stream[index][1]
                if msg[0] & 0xf0 == 0x90 and msg[2]:
                    active.add(msg[1])
                elif msg[0] & 0xf0 == 0x80:
                    active.remove(msg[1])
                index += 1
            # Extra3ticks before each6tick guard are note-off release space.
            if any(boundary - 9 <= tick < boundary for boundary in range(START, END + 1, 120)):
                assert not active, (channel, tick)
        assert not active
    assert [m[1] for t, m in decoded[15] if m[0] == 0xcf and 1 <= m[1] <= 8] == [1,2,3,4,5,6,7,8,1]
    return source, payload, timing
