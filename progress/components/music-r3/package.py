#!/usr/bin/env python3
"""Portable fail-closed source archive. This does not publish or activate music."""
from pathlib import Path
import json,sys,subprocess,zipfile,hashlib
H=Path(__file__).resolve().parent
if sys.flags.optimize:raise RuntimeError('Optimized Python forbidden')
subprocess.run([sys.executable,str(H/'verify.py')],cwd=H,check=True)
import gate_support as g
g.bound_probe_report(H/'evidence/guard-probes.json',H/'REQUIRED-GUARDS.json')
g.bound_probe_report(H/'evidence/packaging-guard-probes.json',H/'REQUIRED-PACKAGING-GUARDS.json')
D=H/'delivery';D.mkdir(exist_ok=True)
# Only receipt-bound complete inputs/source/generated outputs, plus useful proof.
paths=g.source_files()+['SOURCE-INVENTORY.json']+g.files('generated')
paths+=['evidence/current-status.json','evidence/verified-files.json','evidence/host-composition.json','evidence/layouts.json','evidence/stack-audit.json','evidence/phase-sweep.json','evidence/tests.log','evidence/allocation-scan.json','evidence/guard-probes.json','evidence/packaging-guard-probes.json']
paths=sorted(set(paths));g.need(all((H/p).is_file()for p in paths),'Missing deliverable evidence')
manifest={rel:g.sha(H/rel)for rel in paths};name='CaKoOD-Responsive-Music-Transport-Source-Candidate-R3-Transcript-Rebuild-20261006-2317-focused-development.zip';path=D/name
with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for rel in paths:z.write(H/rel,rel)
 z.writestr('ARCHIVE-MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(path)as z:
 g.need(sorted(z.namelist())==sorted(paths+['ARCHIVE-MANIFEST.json']),'Archive member inventory')
 for rel,digest in manifest.items():g.need(hashlib.sha256(z.read(rel)).hexdigest()==digest,'Archive payload changed')
(D/'ARTIFACT.json').write_text(json.dumps(dict(status='PACKAGED_R3_TRANSCRIPT_REBUILD_SOURCE_EMITTED_CANDIDATE',revision=3,path='delivery/'+name,bytes=path.stat().st_size,sha256=g.sha(path),members=len(paths)+1,native_acceptance=False,listening_accepted=False,live_activated=False,rebuild='python3 run.py; python3 verify.py',scope='No emitted resource splice, executable player, new render or activation'),indent=2)+'\n')
print(path.name,g.sha(path),flush=True)
