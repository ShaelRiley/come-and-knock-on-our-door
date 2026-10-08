"""Original deterministic group-timbre renderer. No intelligible TTS or puzzle state.

The compatible schedule/render/sync_patch API is independent of all eight
accepted principal profiles. A plan is a JSON-serializable value.
"""
from pathlib import Path
import hashlib
import io
import json
import math
import re
import struct
import wave

HERE = Path(__file__).resolve().parent
PROFILE = json.loads((HERE / 'audience-profile.json').read_text())
RATE = 22050
MAX_TEXT = 500
MAX_TICKS = 1800
PUNCT = {',': 9, ';': 13, ':': 13, '.': 17, '!': 19, '?': 21, '…': 24, '—': 15, '–': 12, '-': 4}

def base36(n, width):
    if not isinstance(n, int) or n < 0:
        raise ValueError('Nonnegative integer required')
    value = ''
    while n:
        value = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'[n % 36] + value
        n //= 36
    if len(value) > width:
        raise ValueError('Audio36 field overflow')
    return (value or '0').rjust(width, '0')

def patch_name(module, noun, verb=1, cond=0, seq=1):
    if not (0 <= module < 36**3 and all(0 <= x <= 255 for x in (noun, verb, cond)) and 0 <= seq < 36):
        raise ValueError('Audio36 tuple outside existing filename/kernel range')
    return '@' + base36(module, 3) + base36(noun, 2) + base36(verb, 2) + '.' + base36(cond, 2) + base36(seq, 1)

def schedule(line_id, speaker, text):
    if speaker != 'audience':
        raise ValueError('This separate renderer accepts only canonical audience')
    if not isinstance(text, str) or not text.strip() or len(text) > MAX_TEXT:
        raise ValueError('Expected an exact supplied caption fragment of 1..500 characters')
    if '{' in text or '}' in text:
        raise ValueError('Unbound template: supply an observed finite variant first')
    p = PROFILE
    tick = p['lead_ticks']
    pulses = []
    index = 0
    for token in re.finditer(r"[\w]+(?:['’][\w]+)*|[^\w\s]", text, re.UNICODE):
        word = token.group()
        if not any(c.isalnum() for c in word):
            tick += PUNCT.get(word, 0)
            continue
        letters = word.lower()
        count = max(1, len(re.findall(r'[aeiouy]+', letters)))
        if len(letters) > 3 and letters.endswith('e') and not letters.endswith(('le', 'ee')) and count > 1:
            count -= 1
        for syllable in range(count):
            duration = p['pulse_ticks'] + (sum(map(ord, letters)) + syllable) % 3 - 1
            step = p['pitch_steps'][index % len(p['pitch_steps'])]
            if token.end() == len(text) or text[token.end():token.end()+1] in ('.', '!', '?'):
                step += 2 if text[token.end():token.end()+1] == '?' else -2
            pulses.append(dict(start=tick, end=tick + duration, step=step,
                               source_start=token.start(), source_end=token.end(), word=word))
            tick += duration + p['gap_ticks'] + max(v['delay_ticks'] for v in p['voices'])
            index += 1
        tick += p['word_gap_ticks']
    tick += p['tail_ticks']
    if not pulses or tick > MAX_TICKS:
        raise ValueError('Expected spoken words within 1800 ticks; paginate first')
    return dict(schema=1, line_id=line_id, speaker='audience', speaker_id='audience',
                display_name='Audience', text=text, profile_id=p['id'],
                profile_sha256=hashlib.sha256((HERE/'audience-profile.json').read_bytes()).hexdigest(),
                duration_ticks=tick, sample_rate=RATE, pulses=pulses,
                mouth_events=[dict(tick=0, pose=0), dict(tick=tick, pose=0)],
                runtime_speaker_number=0, approximate_syllables=True,
                intelligible_words=False, mouth_view=None,
                sync='Audio36 DoAudio(6) position at 60 Hz')

def render(plan):
    if plan != schedule(plan['line_id'], plan['speaker'], plan['text']):
        raise ValueError('Plan differs from deterministic schedule or current original profile')
    p = PROFILE
    samples = [0.0] * round(plan['duration_ticks'] * RATE / 60)
    harmonic_sum = sum(p['harmonics'])
    for pulse in plan['pulses']:
        for voice in p['voices']:
            start = round((pulse['start'] + voice['delay_ticks']) * RATE / 60)
            end = round((pulse['end'] + voice['delay_ticks']) * RATE / 60)
            n = end - start
            phase = voice['phase']
            base = voice['pitch_hz'] * 2 ** (pulse['step'] / 12)
            for j in range(n):
                t = j / RATE
                attack = min(1, j / (RATE * p['attack_seconds']))
                release = min(1, (n - 1 - j) / (RATE * p['release_seconds']))
                envelope = (0.5 - 0.5 * math.cos(math.pi * max(0, attack))) * (0.5 - 0.5 * math.cos(math.pi * max(0, release)))
                envelope *= math.exp(-p['decay'] * j / max(1, n - 1))
                frequency = base * (1 + voice['vibrato_depth'] * math.sin(2 * math.pi * voice['vibrato_hz'] * t + voice['phase']))
                phase += 2 * math.pi * frequency / RATE
                tone = sum(a * math.sin((h + 1) * phase) for h, a in enumerate(p['harmonics'])) / harmonic_sum
                samples[start+j] += p['gain'] * voice['gain'] * envelope * tone
    pcm = [round(x * 32767) for x in samples]
    if max(map(abs, pcm)) > round(p['gain'] * 32767):
        raise ValueError('Unexpected amplitude/overlap violates synthesis bound')
    out = io.BytesIO()
    with wave.open(out, 'wb') as stream:
        stream.setnchannels(1)
        stream.setsampwidth(2)
        stream.setframerate(RATE)
        stream.writeframes(struct.pack('<' + 'h' * len(pcm), *pcm))
    return out.getvalue()

def sync_patch(plan):
    if plan['runtime_speaker_number'] != 0 or plan['mouth_events'] != [dict(tick=0, pose=0), dict(tick=plan['duration_ticks'], pose=0)]:
        raise ValueError('Audience must never animate a principal mouth')
    return bytes((0x8e, 0)) + b''.join(struct.pack('<hh', e['tick'], e['pose']) for e in plan['mouth_events']) + struct.pack('<h', -1)

def pose_at(plan, tick):
    return 0

def select_observed_fragments(word_ids, manifest):
    """Pure observed-order lookup, requiring all three actual p12VisibleWord values.

    The caller obtains values from p12VisibleWord(0), (1), (2) at presentation
    time. This lookup has no world/desired-order input and no fallback. A host
    still has to validate current eligibility; this function grants no receipt.
    """
    if not isinstance(word_ids, (list, tuple)) or len(word_ids) != 3 or any(type(v) is not int for v in word_ids) or set(word_ids) != {1, 2, 3}:
        raise ValueError('Three distinct actual observed word IDs are required')
    rows = [row for row in manifest['speech'] if row['binding'] and row['binding']['word_ids'] == list(word_ids)]
    if not rows:
        raise ValueError('No exact observed variant; no default binding')
    return rows
