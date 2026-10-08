#!/usr/bin/env python3
"""Move the Porch Conservatory label and its hit rectangle above the screen.

Three constants only, with complete method guards. No runtime or save mutation.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re

HERE = Path(__file__).resolve().parent
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|;[^\n]*|[()]|[^\s();]+')


def method_spans(source):
    tokens = [m for m in TOKEN.finditer(source) if not m.group().startswith(';')]
    result = {}
    for i, token in enumerate(tokens):
        if token.group() != '(' or i + 3 >= len(tokens) or tokens[i + 1].group() != 'method':
            continue
        name = tokens[i + 3].group()
        depth = 0
        for end in tokens[i:]:
            depth += (end.group() == '(') - (end.group() == ')')
            if depth == 0:
                if name in result:
                    raise ValueError('Duplicate method: ' + name)
                result[name] = (token.start(), end.end())
                break
        else:
            raise ValueError('Unclosed method: ' + name)
    return result


def transform(source, reverse=False):
    contract = json.loads((HERE / 'EXIT-DELTA.json').read_text())
    spans = method_spans(source)
    replacements = []
    for item in contract['methods']:
        name = item['name']
        if name not in spans:
            raise ValueError('Missing method: ' + name)
        start, end = spans[name]
        before, after = item['before'], item['after']
        if reverse:
            before, after = after, before
        if source[start:end] != before:
            raise ValueError('Changed or already applied method: ' + name)
        replacements.append((start, end, after))
    for start, end, after in sorted(replacements, reverse=True):
        source = source[:start] + after + source[end:]
    return source


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('main_source', type=Path)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--reverse', action='store_true')
    args = parser.parse_args()
    if args.main_source.is_symlink():
        raise ValueError('Symlink target refused')
    source = args.main_source.read_text()
    changed = transform(source, args.reverse)
    if not args.check:
        temporary = args.main_source.with_name(args.main_source.name + '.porch-exit-tmp')
        temporary.write_text(changed)
        os.replace(temporary, args.main_source)
    print('GUARD_CHECK_PASS' if args.check else 'PATCH_APPLIED',
          hashlib.sha256(source.encode()).hexdigest(),
          hashlib.sha256(changed.encode()).hexdigest())


if __name__ == '__main__':
    main()
