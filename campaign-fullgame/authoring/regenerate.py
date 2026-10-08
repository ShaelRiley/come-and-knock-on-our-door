#!/usr/bin/env python3
"""Regenerate the bounded editable asset set. Never changes canonical game inputs."""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor
import hashlib
import io
import json
import math
from pathlib import Path
import struct
import sys
import wave
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent

def sha(data):
    return hashlib.sha256(data).hexdigest()

def speech_pair(row):
    import voice, audience
    renderer = audience if row['speaker'] == 'audience' else voice
    plan = renderer.schedule(row['line_id'], row['speaker'], row['text'])
    return {row['audio_file']: renderer.render(plan), row['sync_file']: renderer.sync_patch(plan)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='Fresh output directory outside the source tree')
    parser.add_argument('--only', choices=['all', 'speech', 'primitives', 'cadence', 'chime', 'physical'], default='all')
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--allow-changes', action='store_true', help='Allow edited recipes to differ from the canonical pins; never report an exact match')
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()):
        raise SystemExit('Output must be a fresh empty directory')
    package = HERE.parent.resolve()
    if output == package or package in output.parents:
        raise SystemExit('Output must be outside the published source package')
    if not 1 <= args.workers <= 32:
        raise SystemExit('Workers must be between 1 and 32')
    output.mkdir(parents=True, exist_ok=True)
    resources = output/'resources'; resources.mkdir()
    audio = output/'audio'; audio.mkdir()
    def write(files, destination):
        for name, data in files.items():
            (destination/name).write_bytes(data)
    if args.only in ('all', 'primitives'):
        import font_palette, view_writer, midi, safe_midi, credit_midi, midi_mix
        font0 = font_palette.font_resource(json.loads((HERE/'glyphs.json').read_text()))
        font1 = bytearray(font0)
        for char, rows in json.loads((HERE/'lowercase-punctuation.json').read_text()).items():
            position = struct.unpack_from('<H', font1, 6+ord(char)*2)[0]
            if font1[position:position+2] != bytes((6,8)):
                raise ValueError('Unexpected source glyph dimensions')
            font1[position+2:position+10] = bytes([int(row,2)<<3 for row in rows]+[0])
        arrow = json.loads((HERE/'cursor.json').read_text())
        cursor = bytearray(view_writer.encode_view([[view_writer.Cel(10,12,bytes(255 if c=='.' else int(c) for row in arrow for c in row))]]))
        struct.pack_into('<hh', cursor, 38, 5, 11)
        write({'000.font.bin':font0, '001.font.bin':bytes(font1),
               '999.palette.bin':font_palette.palette_resource(json.loads((HERE/'palette.json').read_text())),
               '205.view.bin':bytes(cursor),
               '001.sound.bin':midi_mix.remap_native(safe_midi.make_safe()[1]),
               '002.sound.bin':midi.native_from_smf(midi.source_stinger(),False)[0],
               '003.sound.bin':midi_mix.remap_native(credit_midi.credits()[1]),
               '004.patch.bin':midi.gm_patch()},resources)
        print('Generated 8 original project primitives',flush=True)
    if args.only in ('all', 'physical'):
        import physical_views
        source = package/'source/assets/resources'
        pins = json.loads((HERE/'PHYSICAL-INPUTS.json').read_text())
        for name, expected in pins.items():
            if sha((source/name).read_bytes()) != expected and not args.allow_changes:
                raise ValueError('Physical view input differs: '+name)
        physical_views.generate(source, resources)
        print('Generated 3 physical view resources',flush=True)
    if args.only in ('all', 'cadence'):
        import cadence
        cadence.generate(audio)
        # The atom manifest describes synthesis, but is not itself game audio.
        (audio/'manifest.json').replace(output/'cadence-manifest.json')
        print('Generated 242 cadence audio/sync files',flush=True)
    if args.only in ('all', 'chime'):
        rate = 22050; frames = []
        for i in range(rate*2):
            t = i/rate; value = 0
            for start, frequency in [(0,523.25),(.18,659.25),(.36,783.99),(.60,1046.5)]:
                z = t-start
                if z >= 0:
                    value += .15*min(1,z/.008)*math.exp(-3.8*z)*(math.sin(2*math.pi*frequency*z)+.25*math.sin(2*math.pi*frequency*2*z))
            frames.append(struct.pack('<h',int(max(-1,min(1,value))*32767)))
        with wave.open(str(audio/'@0PS0101.001'),'wb') as stream:
            stream.setparams((1,2,rate,0,'NONE','not compressed'));stream.writeframes(b''.join(frames))
        print('Generated original celebration chime',flush=True)
    if args.only in ('all', 'speech'):
        rows = json.loads((HERE/'speech-recipes.json').read_text())['rows']
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            for index, files in enumerate(executor.map(speech_pair,rows,chunksize=4),1):
                write(files,audio)
                if index%50==0 or index==len(rows):
                    print(f'Generated {index}/{len(rows)} speech pairs',flush=True)
    expected = json.loads((HERE/'EXPECTED-GENERATED.json').read_text())
    files = {str(p.relative_to(output)):{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for d in (resources,audio) for p in sorted(d.iterdir())}
    mismatches = [name for name,row in files.items() if row != expected.get(name)]
    missing = sorted(set(expected)-set(files)) if args.only=='all' else []
    report = {'scope':'Bounded deterministic asset regeneration; no runtime or campaign-state claim',
              'selection':args.only,'files':files,'file_count':len(files),'mismatches':mismatches,'missing':missing,
              'status':'PASS_EXACT_BOUNDED_REGENERATION' if not (mismatches or missing) else 'EDITED_OUTPUT_DIFFERS_FROM_CANONICAL',
              'blanket_rights_clearance':False}
    (output/'REGENERATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(report['status'],len(files),'files',len(mismatches),'mismatches',len(missing),'missing',flush=True)
    if (mismatches or missing) and not args.allow_changes:
        raise SystemExit(1)

if __name__=='__main__':
    main()
