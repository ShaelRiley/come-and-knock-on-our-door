"""Explicit development seal; verifier only reads it and never updates it."""
from pathlib import Path
import hashlib,json
H=Path(__file__).resolve().parents[1];R=H.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
local={}
for p in H.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(H);parts=rel.parts
 if any(x in parts for x in ['__pycache__','.pytest_cache','build','revisions','evidence','release']):continue
 if p.name in ['INPUTS.json','VERIFICATION.json','REVIEW-SNAPSHOT.json']:continue
 if parts[0]=='visual-work' and p.suffix not in ['.inc','.md','.json','.py','.in']:continue
 local[str(rel)]={'sha256':sha(p),'bytes':p.stat().st_size}
external={}
paths=[R/'p03-editable-checkpoint/toolchain/scicompile',R/'p05-domain-reconstruction/tools/emitted_gates.py',R/'p04-native-inventory-fix-reconstruction/tests/render_regressions.py']
for dir in ['p04-native-inventory-fix-reconstruction/staging-proof/src','p04-native-inventory-fix-reconstruction/staging-proof/verification-checkpoint','p04-native-inventory-fix-reconstruction/reference/accepted/build','p04-native-inventory-fix-reconstruction/inputs/verification','p05-domain-reconstruction/reference']:
 paths += [p for p in (R/dir).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
for n in [304,227]:paths += [next((R/'p05-art-reconstruction').glob(f'**/{n}.view.bin'))]
for p in paths:external[str(p.relative_to(R))]={'sha256':sha(p),'bytes':p.stat().st_size}
(H/'INPUTS.json').write_text(json.dumps({'schema':1,'local':dict(sorted(local.items())),'external':dict(sorted(external.items())),'status':'INPUT_IDENTITIES_ONLY_NOT_ACCEPTANCE'},indent=2)+'\n');print(len(local),len(external),sha(H/'INPUTS.json'))
