#!/usr/bin/env python3
"""Opening suffix startup metadata and unchanged musical content.

Resource-format evidence only: no bytecode VM, native playback, pixels, input,
save or campaign acceptance. Run: python -B tests/check_opening_reverb.py
--sound-dir selects private suffix160..168 proposals for diagnosis only.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys
import time
import traceback


def source_root():
    for parent in Path(__file__).resolve().parents:
        if (parent / 'authoring/score/recovered/tools/music_generate.py').is_file():
            return parent
    raise RuntimeError('Cannot locate game source')


SOURCE = source_root()
sys.path.insert(0, str(SOURCE / 'authoring/score/recovered/tools'))
from music_generate import decode_sound

SOURCE100 = '7ca33efb45bcccb6d49cccf695a83a7722512906435b5f5e6ad3c1bdb4677906'
# Frozen approved R11 noncontrol channel bytes/events, excluding ONLY ch15
# startup metadata. These do not derive expected music from the candidate.
EXPECTED = {
    160: ('3e3f0c880146e60647c8eb97d6d3c0c9caa2c92e90678a56d6185246d289a38f', '1f7ee870916974c69e04ed93e7ce74831c27dbfb9e0133f4b3ac51f8ff4a8aa0', 1192),
    161: ('ac4b0d3bf5cf096145a103042dd5d4458ddb10fbde31701889b651d0f4fd4a6e', '8559b148918dc4b15b768a6eb89e7dd7a7a9932958c5fb7f87804cb4766e3ebd', 1058),
    162: ('ec7e54b18d3c5e0f405b807f976f1785b9097c61650c8ba4f7b4a4470bc692ec', '1f4ab9e0b8fb4cef08e2e0f4c5162c9ea700aa20330d9c9bbf329af4f27ba51d', 933),
    163: ('2ebb3855902801bd518f8c12a71ad3e2e7ddbbffdacb5bb495e3a3b1164f6aa0', 'adb4bede8d50b9ac0f6822bb3fd0ffacdf575f149fcb74eb1be776b33ee47a42', 808),
    164: ('649fffc963fd49edd976d1b839a87a4803fc2793d464b17e375a7e4409b1fd51', '3a4ed6a635d5b9845b23514200763fd9b5cf2340a16c4af8353fae339cbcd0af', 675),
    165: ('43bd07f9e620f244d9a93c6c8c2a86b789e292049fb262c9d608be228775f7a6', 'fe4b0d607725d49bc64e65a260f4ea3d944522f5a519088492650c9af10caf0c', 547),
    166: ('81de29ec4b3e14c135bd6e9b86b2272a39b8d4c6205faa891c93ee8684cf01f5', 'd21d3b60639986c93f451963b4cd668c8ede6c06dd95b198977243296865d1e1', 415),
    167: ('bdd2ee8cd85e004595d1c184f31e2650e8cdb9954b972fb59c1f07585b7e95e0', 'a6001f4be059174a1520b9dc384bd94175fd817495f36504d8420d0d51c0ac11', 286),
    168: ('cc522ad4fb341ee2fad592e696ce58144f1f6b4bf68857db65a4193e15d1ae8a', '9803a89298b13b38ee34cf4c7d31a6bc15a7cbad58072d41f3aaadb6c485c403', 150),
}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def normalized_digest(value):
    return digest(json.dumps(value, sort_keys=True, separators=(',', ':')).encode())


def tracks(raw):
    assert raw and raw[0] == 7, 'Expected SCI track07'
    pos, result = 1, {}
    while raw[pos:pos + 2] != b'\xff\xff':
        assert pos + 6 <= len(raw), 'Truncated track descriptor'
        unused, offset, size = struct.unpack_from('<HHH', raw, pos)
        assert not unused and size >= 2 and offset + size <= len(raw), 'Invalid track descriptor'
        payload = raw[offset:offset + size]
        channel = payload[0] & 15
        assert channel not in result, 'Duplicate channel'
        result[channel] = payload
        pos += 6
    return result


def startup_reverb(channel_tracks):
    # Stock SCI SoundResource strips the raw two-byte channel header. The MIDI
    # parser getSongReverb reads signed control EVENT data[6], not rawtrack[6].
    data = channel_tracks[15][2:]
    assert len(data) > 6, 'Truncated SCI control startup data'
    return struct.unpack('b', data[6:7])[0]


def run(sound_dir, detail):
    base = (SOURCE / 'assets/resources/100.sound.bin').read_bytes()
    assert digest(base) == SOURCE100, 'Approved complete opening100 changed'
    assert (SOURCE / 'authoring/score/assets/100.sound.bin').read_bytes() == base, 'Opening100 mirror differs'
    assert startup_reverb(tracks(base)) == 0, 'Opening100 startup metadata differs'
    detail['source100_sha256'] = SOURCE100
    rows, failures = [], []
    for number, expected in EXPECTED.items():
        path = sound_dir / (str(number) + '.sound.bin')
        raw = path.read_bytes()
        channel_tracks = tracks(raw)
        value = startup_reverb(channel_tracks)
        events = decode_sound(raw)
        noncontrol_tracks = {ch: value.hex() for ch, value in channel_tracks.items() if ch != 15}
        musical = {ch: [[tick, msg.hex()] for tick, msg in seq]
                   for ch, seq in events.items() if ch != 15}
        actual = (normalized_digest(noncontrol_tracks), normalized_digest(musical),
                  sum(len(seq) for seq in musical.values()))
        assert actual == expected, 'Musical raw bytes/events/ticks changed: ' + str(number)
        end = 3600 - (number - 159) * 360
        row = {'resource': number, 'startup_reverb': value, 'driver_admissible': value < 11,
               'noncontrol_raw_sha256': actual[0], 'normalized_event_sha256': actual[1],
               'musical_events': actual[2], 'terminal_tick': end, 'sha256': digest(raw)}
        rows.append(row)
        if value >= 11:
            failures.append('resource' + str(number) + ': stock SCI setReverb requires <11; actual=' + str(value))
        elif value != 0:
            failures.append('resource' + str(number) + ': missing explicit source reverb0 startup metadata; actual=' + str(value))
        expected_control = [(0, b'\xcf\x00'), (0, b'\xbf\x50\x00'), (end, b'\xbf\x50\x00')]
        if events[15] != expected_control:
            failures.append('resource' + str(number) + ': source startup/terminal control sequence differs')
        if sound_dir == SOURCE / 'assets/resources':
            assert (SOURCE / 'authoring/score/assets' / path.name).read_bytes() == raw, 'Suffix mirror differs'
    detail.update(rows=rows, musical_event_count=sum(r['musical_events'] for r in rows),
                  all_noncontrol_raw_bytes_events_and_ticks_unchanged=True)
    assert not failures, '; '.join(failures)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sound-dir', type=Path, default=SOURCE / 'assets/resources')
    args = parser.parse_args()
    started = time.monotonic()
    detail = {'case': 'opening_reverb', 'evidence_kind': 'RESOURCE_FORMAT_AND_APPROVED_MUSICAL_CONTENT',
              'executes_emitted_bytecode': False, 'native_acceptance': False,
              'scope': 'Nine real SCI suffix startup headers, source100 identity and approved noncontrol raw/event/tick equality. No native playback or game progression.'}
    try:
        run(args.sound_dir.resolve(), detail)
        detail['status'], code = 'PASS', 0
    except Exception as error:
        detail.update(status='FAIL', error=repr(error), traceback=traceback.format_exc())
        code = 1
    detail.update(elapsed_seconds=round(time.monotonic() - started, 6), exit_code=code)
    print(json.dumps(detail, indent=2))
    return code


if __name__ == '__main__':
    sys.exit(main())
