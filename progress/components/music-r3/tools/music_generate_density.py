#!/usr/bin/env python3
"""Separate original eight-role/tempo-bridge SCI stress fixture, IDs11 and12.

Does not overwrite generated/ or the frozen run1 resources. All source notes
are new diagnostic composition; high-density chord/drum bursts are stress
material rather than a proposed finished musical arrangement.
"""
from fractions import Fraction
import json
from pathlib import Path
import struct

import generate as g

OUT = g.HERE / 'generated-density'
START = 77  # source PPQ ticks at96BPM, about100.26ms of setup silence
BAR = 4 * g.PPQ
BRIDGE_BAR = 12
LOOP_BAR = 13
END_BAR = 21
ROLES = [
    {'name': 'BASS', 'channel': 0, 'program': 32, 'volume': 80, 'pan': 64, 'voices': 1},
    {'name': 'PULSE', 'channel': 1, 'program': 0, 'volume': 60, 'pan': 48, 'voices': 3},
    {'name': 'HARMONY', 'channel': 2, 'program': 48, 'volume': 45, 'pan': 74, 'voices': 3},
    {'name': 'HOME_LEAD', 'channel': 3, 'program': 71, 'volume': 70, 'pan': 40, 'voices': 1},
    {'name': 'CHARACTER', 'channel': 4, 'program': 59, 'volume': 68, 'pan': 88, 'voices': 1},
    {'name': 'TEXTURE', 'channel': 5, 'program': 89, 'volume': 40, 'pan': 58, 'voices': 2},
    {'name': 'ACCENT', 'channel': 6, 'program': 11, 'volume': 64, 'pan': 68, 'voices': 6},
    {'name': 'RHYTHM', 'channel': 9, 'program': 0, 'volume': 55, 'pan': 64, 'voices': 6},
]
TEMPO96 = 625000
TEMPO104 = 576923  # integer SMF microseconds;104.000014BPM


def pack_smf(events, end):
    events = [(0, -30, b'\xff\x51\x03' + TEMPO96.to_bytes(3, 'big')),
              (0, -29, b'\xff\x58\x04\x04\x02\x18\x08')] + events
    events += [(end, 99, b'\xff\x2f\x00')]
    body = bytearray()
    previous = 0
    for tick, _, message in sorted(events, key=lambda e: (e[0], e[1])):
        body += g.vlq(tick - previous) + message
        previous = tick
    return b'MThd' + struct.pack('>IHHH', 6, 0, 1, g.PPQ) + b'MTrk' + struct.pack('>I', len(body)) + body


def marker(text):
    payload = text.encode('ascii')
    return b'\xff\x06' + g.vlq(len(payload)) + payload


def make_source(origin=START):
    events, bars = [], []
    def add(t, msg, priority=1):
        events.append((t, priority, bytes(msg)))
    def note(t, length, ch, pitch, velocity=58):
        add(t, [0x90 | ch, pitch, velocity], 2)
        add(t + length, [0x80 | ch, pitch, 0], 0)
    def chord(t, length, ch, pitches, velocity=55):
        for pitch in pitches:
            note(t, length, ch, pitch, velocity)
    for role in ROLES:
        ch = role['channel']
        add(0, [0xc0 | ch, role['program']])
        for cc, value in [(7, role['volume']), (10, role['pan']), (64, 0), (1, 0)]:
            add(0, [0xb0 | ch, cc, value])
        add(0, [0xe0 | ch, 0, 64])

    # Eight isolated bars, identified by native cue and manifest, so actual
    # patch/drum output can be distinguished in a capture.
    roll_notes = [[36], [60, 64, 67], [55, 60, 64], [72], [67], [60, 67], [72, 76, 79], [36]]
    for i, role in enumerate(ROLES):
        start = origin + i * BAR
        bars.append({'bar_index': i, 'source_tick': start, 'cue': i + 1, 'section': 'roll_call', 'role': role['name']})
        add(start, marker('ROLE_' + role['name']), -10)
        if role['channel'] == 9:
            for beat, pitch in enumerate([36, 38, 42]):
                note(start + beat * g.PPQ, 100, 9, pitch, 75)
        else:
            chord(start, 380, role['channel'], roll_notes[i], 72)
            chord(start + g.PPQ, 380, role['channel'], [p + 7 for p in roll_notes[i]], 65)

    def ordinary(start, root, climax=False):
        for beat in range(4):
            t = start + beat * g.PPQ
            burst = climax and beat == 0
            #17 held notes ordinarily,23 for the brief first climax beat.
            note(t, 260, 0, root - 12, 62)
            chord(t, 260, 1, [root, root + 4, root + 7], 48)
            chord(t, 260, 2, [root + 7, root + 12, root + 16], 43)
            note(t, 260, 3, root + 24 + [0, 2, 4, 7][beat], 59)
            note(t, 260, 4, root + 19 - [0, 2, 0, 3][beat], 57)
            chord(t, 260, 5, [root + 12, root + 19], 37)
            pitches = [root + 12, root + 16, root + 19]
            if burst:
                pitches += [root + 24, root + 28, root + 31]
            chord(t, 200, 6, pitches, 48 if not burst else 55)
            drums = [36, 38, 42, 46, 49, 51] if burst else [36, 38, 42]
            chord(t, 100, 9, drums, 43 if not burst else 56)

    for i, root in zip(range(8, 12), [48, 53, 55, 48]):
        start = origin + i * BAR
        bars.append({'bar_index': i, 'source_tick': start, 'cue': 20 + i - 8, 'section': 'ordinary_96'})
        add(start, marker('ORDINARY_96_' + str(i - 7)), -10)
        ordinary(start, root)

    # One real composed transition bar: dominant pedal, rising pickup, less
    # texture, tempo changes at its four authored beats, then resolution toC.
    start = origin + BRIDGE_BAR * BAR
    bars.append({'bar_index': BRIDGE_BAR, 'source_tick': start, 'cue': 30, 'section': 'bridge_96_to_104'})
    for beat, tempo in enumerate([625000, 608108, 592105, TEMPO104]):
        add(start + beat * g.PPQ, b'\xff\x51\x03' + tempo.to_bytes(3, 'big'), -20)
        note(start + beat * g.PPQ, 220, 0, 43 if beat < 2 else 50, 62)
        chord(start + beat * g.PPQ, 200, 1, [55, 59, 62], 49)
        note(start + beat * g.PPQ, 160, 3, [67, 69, 71, 74][beat], 64)
        note(start + beat * g.PPQ, 80, 9, 42, 37)
    for n, pitch in enumerate([67, 71, 74, 76]):
        note(start + 3 * g.PPQ + n * 90, 65, 6, pitch, 61)
    add(start, marker('BRIDGE_DOMINANT_PICKUP'), -10)

    for j, root in enumerate([48, 53, 55, 48, 57, 53, 55, 48]):
        i = LOOP_BAR + j
        start = origin + i * BAR
        bars.append({'bar_index': i, 'source_tick': start, 'cue': 40 + j,
                     'section': 'climax_104' if j == 3 else 'ordinary_104',
                     'climax_only_first_beat': j == 3})
        label = 'CLIMAX' if j == 3 else 'ORDINARY_104_' + str(j + 1)
        add(start, marker(('LOOP_IN_' if j == 0 else '') + label), -10)
        ordinary(start, root, climax=j == 3)
    end = origin + END_BAR * BAR
    add(end, marker('LOOP_OUT'), -10)
    return pack_smf(events, end), bars, end


def source_times(smf):
    ppq, events = g.parse_smf(smf)
    tempo, previous, elapsed = 500000, 0, Fraction(0)
    result, tempo_map = {}, []
    for source_tick, _, message in events:
        elapsed += Fraction((source_tick - previous) * tempo, ppq)
        previous = source_tick
        scaled = elapsed / g.SCI_TICK_US
        tick = (scaled.numerator * 2 + scaled.denominator) // (2 * scaled.denominator)
        result[source_tick] = {'sci_tick': tick, 'source_us': float(elapsed),
                               'absolute_quantization_error_us': float(abs(tick * g.SCI_TICK_US - elapsed))}
        if message[:2] == b'\xff\x51':
            tempo = int.from_bytes(message[2:], 'big')
            tempo_map.append({'source_tick': source_tick, 'source_us': float(elapsed),
                              'microseconds_per_quarter': tempo, 'bpm': 60000000 / tempo})
    return result, tempo_map


def held_profile(channels):
    active = set()
    profile = []
    events = sorted([(tick, channel, msg) for channel, stream in channels.items() for tick, msg in stream],
                    key=lambda e: (e[0], 0 if e[2][0] & 0xf0 == 0x80 else 1, e[1]))
    for tick, ch, msg in events:
        kind = msg[0] & 0xf0
        if kind == 0x90 and msg[2]:
            if (ch, msg[1]) in active:
                raise AssertionError('Overlapping same pitch')
            active.add((ch, msg[1]))
        elif kind == 0x80 or (kind == 0x90 and msg[2] == 0):
            if (ch, msg[1]) not in active:
                raise AssertionError('Unmatched note off')
            active.remove((ch, msg[1]))
        profile.append((tick, len(active)))
    if active:
        raise AssertionError('Hanging notes')
    return profile


def make_native(start_source_tick=START, guard_ticks=3):
    smf, bars, end = make_source(start_source_tick)
    midi, timing = g.convert_smf(smf)
    positions, tempos = source_times(smf)
    channels = {}
    for tick, msg in midi:
        channels.setdefault(msg[0] & 15, []).append((tick, msg))
    for bar in bars:
        bar.update(positions[bar['source_tick']])
        bar['guard_tick'] = bar['sci_tick'] - guard_ticks
        bar['nominal_sci_seconds'] = bar['sci_tick'] * g.SCI_TICK_US / 1000000
    loop_tick = bars[LOOP_BAR]['sci_tick']
    end_tick = positions[end]['sci_tick']
    control = [(0, b'\xcf\0'), (0, b'\xbf\x50\0')]
    control += [(bar['guard_tick'], bytes((0xcf, bar['cue']))) for bar in bars]
    control += [(loop_tick, b'\xbf\x50\0'), (loop_tick, b'\xcf\x7f'),
                (end_tick - guard_ticks, bytes((0xcf, 40))), (end_tick, b'\xbf\x50\0')]
    channels[15] = sorted(control, key=lambda e: e[0])
    voices = {r['channel']: r['voices'] for r in ROLES}
    payload = g.sound_resource(channels, voices)
    decoded = g.decode_sound(payload)
    profile = held_profile(decoded)
    maxima = {}
    for i, bar in enumerate(bars):
        limit = bars[i + 1]['sci_tick'] if i + 1 < len(bars) else end_tick
        bar['maximum_held_notes'] = max(n for t, n in profile if bar['sci_tick'] <= t < limit)
        maxima[bar['section']] = max(maxima.get(bar['section'], 0), bar['maximum_held_notes'])
        # All melodic AND drum note-offs precede each native3-tick guard.
        active = set()
        for tick, channel, msg in sorted([(t, c, m) for c, es in decoded.items() for t, m in es], key=lambda e: e[0]):
            if tick > bar['guard_tick']:
                break
            kind = msg[0] & 0xf0
            if kind == 0x90 and msg[2]:
                active.add((channel, msg[1]))
            elif kind == 0x80:
                active.discard((channel, msg[1]))
        assert not active, ('guard not note-silent', bar)
    assert maxima['ordinary_96'] == 17 and maxima['ordinary_104'] == 17
    assert maxima['climax_104'] == 23
    assert set(decoded) == {0, 1, 2, 3, 4, 5, 6, 9, 15}
    assert max(n for _, n in profile) == 23
    return smf, payload, timing, bars, tempos, end_tick, maxima


def make_stinger():
    ev = [(0, 0, b'\xc7\x09'), (0, 0, b'\xb7\x07\x50'),
          (0, 0, b'\xb7\x0a\x40'), (0, 0, b'\xb7\x40\0'),
          (77, 2, b'\x97\x54\x48'), (385, 0, b'\x87\x54\0')]
    smf = pack_smf(ev, 768)
    midi, timing = g.convert_smf(smf)
    end_tick = source_times(smf)[0][768]['sci_tick']
    channel = [(t, m) for t, m in midi]
    payload = g.sound_resource({7: channel, 15: [(0, b'\xcf\0'), (0, b'\xbf\x50\0'),
                                               (end_tick, b'\xbf\x50\0')]}, {7: 1, 15: 0})
    assert max(n for _, n in held_profile(g.decode_sound(payload))) == 1
    return smf, payload, timing


def build(output=OUT, start_source_tick=START, guard_ticks=3):
    for sub in ('source', 'payloads', 'patches'):
        (output / sub).mkdir(parents=True, exist_ok=True)
    written = {}
    def emit(name, data):
        (output / name).write_bytes(data)
        written[name] = {'bytes': len(data), 'sha256': g.sha(data)}
    smf, payload, timing, bars, tempos, end_tick, maxima = make_native(start_source_tick, guard_ticks)
    emit('source/density-bed.mid', smf)
    emit('payloads/011.sound.bin', payload)
    emit('patches/sound.011', b'\x84\0' + payload)
    emit('source/density-timing.json', (json.dumps(timing, indent=2) + '\n').encode())
    sting_smf, sting, sting_timing = make_stinger()
    emit('source/density-stinger.mid', sting_smf)
    emit('payloads/012.sound.bin', sting)
    emit('patches/sound.012', b'\x84\0' + sting)
    emit('payloads/004.patch.bin', g.gm_patch())
    emit('patches/patch.004', b'\x89\0' + g.gm_patch())
    pcm = (g.ROOT / 'assets/proof/audience_lane_test.wav').read_bytes()
    emit('patches/@0010101.001', pcm)
    loop_tick = bars[LOOP_BAR]['sci_tick']
    manifest = {'status': 'original static density/bridge fixture; native output/voice ownership/tempo capture pending',
                'resource_ids': {'bed': 11, 'stinger': 12, 'identity_gm_patch': 4},
                'source_ppq': g.PPQ, 'native_tick_us': g.SCI_TICK_US,
                'provenance': 'New original diagnostic notes; no commercial resources. PCM is existing original synthetic chuff. Brief accent/percussion stacks are deliberately diagnostic stress material, not final score orchestration.',
                'roles': ROLES, 'optional_stinger': {'channel': 7, 'program': 9, 'maximum_held_notes': 1, 'start_delay_ticks': 6},
                'allocator': {'normal_melodic_channels': 8, 'bed_melodic_channels': 7, 'stinger_melodic_channels': 1,
                              'fixed_percussion_channel_zero_based': 9, 'percussion_header': '0x29: channel9 with native flag2',
                              'declared_bed_voices': sum(r['voices'] for r in ROLES), 'declared_bed_plus_stinger_voices': sum(r['voices'] for r in ROLES) + 1,
                              'native_driver_voice_budget': 32, 'static_assignment_fits': True,
                              'native_patch_ownership_and_physical_synthesis_voices': 'pending capture/profiling'},
                'maximum_held_notes_by_section': maxima, 'ordinary_plus_stinger_max': 18, 'climax_plus_stinger_max': 24,
                'note_budget_caveat': 'Key-held MIDI note counts include percussion but do not measure sounding release tails or layered FluidSynth voices.',
                'tempo_map': tempos, 'bars': bars,
                'markers': {'START': 0, 'LOOP_IN': loop_tick, 'LOOP_OUT': end_tick, 'END': end_tick,
                    'REJOIN': [b['sci_tick'] for b in bars], 'EXIT_BAR': [b['guard_tick'] for b in bars],
                    'EXIT_PHRASE': [b['guard_tick'] for b in bars if b['bar_index'] in (8, 12, 13, 17)],
                    'BRIDGE': bars[BRIDGE_BAR]['sci_tick'], 'ACCENT': bars[LOOP_BAR + 3]['sci_tick']},
                'loop': {'start_tick': loop_tick, 'end_tick': end_tick,
                    'length_ticks': end_tick - loop_tick, 'nominal_native_seconds': (end_tick - loop_tick) * g.SCI_TICK_US / 1000000,
                    'end_guard_tick': end_tick - guard_ticks, 'end_guard_cue': 40, 'repeat_cues': list(range(40, 48))},
                'maximum_absolute_event_quantization_error_us': max(row['error_us'] for row in timing),
                'guard_ticks': guard_ticks, 'all_authored_guards_note_silent': True, 'all_notes_balanced': True,
                'integration': 'Separate density-game only. Accept cues1..8,20..23,30,40..47. Use Sound11 and12. Initial muted play requires explicitDoSound8object0; raise whole-volume at first cue1. No fixed120-tick scheduler assumptions. Stinger adds at mostone held note even during climax.',
                'files': written}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


if __name__ == '__main__':
    manifest = build()
    print(json.dumps({k: manifest[k] for k in ('resource_ids', 'allocator', 'maximum_held_notes_by_section',
                                              'tempo_map', 'loop', 'maximum_absolute_event_quantization_error_us')}, indent=2))
