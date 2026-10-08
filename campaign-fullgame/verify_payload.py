#!/usr/bin/env python3
"""Verify exact public component membership, bytes and executable modes."""
from pathlib import Path
import hashlib,json,sys
H=Path(__file__).resolve().parent
if sys.flags.optimize:raise RuntimeError('Optimized Python is unsupported')
expected=json.loads((H/'INTEGRATION-INVENTORY.json').read_text())['files'];actual={}
for p in sorted(H.rglob('*')):
 if p.is_symlink():raise RuntimeError('Symlink in payload')
 if p.is_file() and p!=H/'INTEGRATION-INVENTORY.json':actual[str(p.relative_to(H))]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'executable':bool(p.stat().st_mode&0o111)}
if actual!=expected:raise RuntimeError('Public membership, bytes or executable modes changed')
print('PASS_PUBLIC_PAYLOAD',len(actual),'files')
