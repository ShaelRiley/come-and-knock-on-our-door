#!/usr/bin/env python3
"""Check exact published campaign membership, bytes, file sizes and POSIX modes."""
from pathlib import Path
import hashlib,json,sys
H=Path(__file__).resolve().parent
if sys.flags.optimize:raise RuntimeError('Optimized Python is forbidden')
manifest=H/'INTEGRATION-INVENTORY.json'
expected=json.loads(manifest.read_text())['files'];actual={}
for p in sorted(H.rglob('*')):
 if p.is_symlink():raise RuntimeError('Symlink in campaign payload')
 if p.is_file() and p!=manifest:
  actual[str(p.relative_to(H))]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mode':format(p.stat().st_mode&0o777,'04o'),'executable':bool(p.stat().st_mode&0o111)}
if actual!=expected:raise RuntimeError('Campaign membership, bytes, size or POSIX mode changed')
print('PASS_CAMPAIGN_PAYLOAD',len(actual),'files plus inventory')
