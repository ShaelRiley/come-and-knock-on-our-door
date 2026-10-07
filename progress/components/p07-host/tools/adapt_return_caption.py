#!/usr/bin/env python3
"""Guarded, reversible source-only correction. Never write to input paths."""
from pathlib import Path
import argparse, hashlib, json, sys, difflib
sys.dont_write_bytecode = True
H = Path(__file__).resolve().parent
sys.path.insert(0, str(H / 'tools'))
from source_tools import methods

BASE_MAIN_SHA = '0533b604ce03f416384c6bb31d3e033077c96c40fbc67ed9d44c82027f05b8e6'
BASE_WALK_SHA = '2285e0ebb3815834bc166d40860e299556b83ce7e7cfd70917ef2c5f27766024'
sha = lambda b: hashlib.sha256(b).hexdigest()

def transform(source):
    old = methods(source)['walk']
    if sha(old.encode()) != BASE_WALK_SHA:
        raise ValueError('walk differs from the exact accepted method; refuse a stale or repeated patch')
    replacements = [
        ('(method (walk obj)', '(method (walk obj &tmp returning)'),
        ('            (= location 1) (= tray 2) (= traySafe 1) (= houseEntered 1)',
         '            (= returning houseEntered)\n'
         '            (= location 1) (= tray 2) (= traySafe 1) (= houseEntered 1)'),
        ('            (self say: 36) (return 0))',
         '            ; Preserve the production arrival only on genuine first entry.\n'
         '            ; Later arrivals reuse the existing silent room navigation notice.\n'
         '            (if returning (self speechCancel:) (self navNoticeSet: 134 1)\n'
         '            else (self say: 36)) (return 0))'),
    ]
    new = old
    for before, after in replacements:
        if new.count(before) != 1:
            raise ValueError('Expected unique source anchor is missing or duplicated')
        new = new.replace(before, after, 1)
    if source.count(old) != 1:
        raise ValueError('Method occurrence is not unique')
    result = source.replace(old, new, 1)
    a, b = methods(source), methods(result)
    if set(a) != set(b) or [n for n in a if a[n] != b[n]] != ['walk']:
        raise ValueError('Correction scope escaped the walk method')
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, default=H.parent/'p05-host-reconstruction/src/main.sc')
    parser.add_argument('--output', type=Path, default=H/'src/main.sc')
    args = parser.parse_args()
    if not args.output.resolve().is_relative_to(H) or args.output.resolve() == args.input.resolve():
        raise ValueError('Output must be a separate file inside this adapter workspace')
    original = args.input.read_bytes()
    result = transform(original.decode()).encode()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(result)
    (H/'fixtures/main.after.sc').write_bytes(result)
    (H/'evidence/source.diff').write_text(''.join(difflib.unified_diff(original.decode().splitlines(True),result.decode().splitlines(True),fromfile='accepted/main.sc',tofile='corrected/main.sc')))
    (H/'evidence/source-adapter.json').write_text(json.dumps({
        'status':'PASS_GUARDED_SOURCE_TRANSFORM','input_sha256':sha(original),
        'output_sha256':sha(result),'exact_accepted_main':sha(original)==BASE_MAIN_SHA,
        'before_walk_sha256':BASE_WALK_SHA,'after_walk_sha256':sha(methods(result.decode())['walk'].encode()),
        'changed_methods':['walk'],'new_persistent_state':False,'new_selectors':False,
        'new_text_or_voice_resources':False,'native_acceptance':False
    },indent=2)+'\n')
    print('PASS_GUARDED_SOURCE_TRANSFORM', sha(result))

if __name__ == '__main__':
    main()
