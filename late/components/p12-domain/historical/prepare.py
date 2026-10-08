#!/usr/bin/env python3
"""Reuse the approved original packer; all outputs stay in this fixture."""
from pathlib import Path
import argparse
import json
import re
import struct
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import pack

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('seed', 'package'))
    args = parser.parse_args()
    text = '\n'.join((HERE/'src'/name).read_text() for name in ('main.sc', 'module994.sc'))
    props = []
    for body in re.findall(r'\(properties\s+([^()]*)\)', text, re.S):
        props.extend(re.sub(r';[^\n]*', '', body).split()[::2])
    methods = re.findall(r'\(method \((\w+)', text)
    for value, name in enumerate(sorted(set(props+methods)-set(pack.SELECTORS)), 8):
        assert value < 4096
        pack.SELECTORS[name] = value
    resources = pack.base_resources()
    # Standalone species0 Game; species1 P12State. Production reserves species16.
    resources[(6, 996)] = struct.pack('<4H', 0, 0, 0, 994)
    out = HERE/'build/seed'
    if args.mode == 'package':
        out = HERE/'build/compile-fixture'
        for number in (0, 994):
            path = HERE/f'build/compiled/{number}.scr.bin'
            resources[(2, number)] = path.read_bytes()
            resources[(17, number)] = Path(str(path)+'.hep').read_bytes()
    pack.pack_resources(resources, out)
    pack.validate_resources(out)
    if args.mode == 'seed':
        for name in ('resource.map', 'resource.000'):
            (HERE/name).write_bytes((out/name).read_bytes())
    (HERE/'selectors.json').write_text(json.dumps(pack.SELECTORS, indent=2, sort_keys=True)+'\n')
    print(f'Packed {len(resources)} original compile resources at {out}')

if __name__ == '__main__':
    main()
