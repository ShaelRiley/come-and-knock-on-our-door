#!/usr/bin/env python3
"""Export short practice topics without changing approved retorts or SCI buffers."""
from pathlib import Path
import hashlib
import json

A = Path(__file__).resolve().parent
S = A.parents[1] / 'source'
config = json.loads((A / 'labels.json').read_text())
assert config['resource'] == 242 and config['first_slot'] == 37
assert config['buffer_words'] == 4 and config['max_data_bytes'] == 7
rows = config['labels']
assert [r['pair_id'] for r in rows] == [f'IR{i:02d}' for i in range(1, 25)]
labels = [r['label'].encode('ascii') for r in rows]
assert len(set(labels)) == 24
assert all(0 < len(label) <= 7 and b'\0' not in label for label in labels)
target = S / 'assets/resources/242.text.bin'
slots = target.read_bytes().split(b'\0')
assert len(slots) == 62 and slots[-1] == b''
prefix = b'\0'.join(slots[:37]) + b'\0'
assert hashlib.sha256(prefix).hexdigest() == config['protected_prefix_sha256']
for i, label in enumerate(labels):
    assert slots[37+i] in (f'IR{i+1:02d}'.encode(), label)
slots[37:61] = labels
target.write_bytes(b'\0'.join(slots))
print('Exported 24 practice topics; approved retorts and menu commands unchanged.')
