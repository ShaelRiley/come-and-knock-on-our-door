"""NEW one-time explicit byte-preserving input materialization; no archive copies."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
R=ROOT.parent
PACKET=Path('/workspace/shared/cakood-context-recovery-batch2/courtyard-models')
P09=Path('/workspace/shared/cakood-context-recovery-batch2/p09-model')
items=[]
def copy(source,destination,classification):
    source=Path(source); destination=ROOT/destination; data=source.read_bytes()
    destination.parent.mkdir(parents=True,exist_ok=True)
    if destination.exists() and destination.read_bytes()!=data:raise RuntimeError(f'Existing bytes differ: {destination}')
    destination.write_bytes(data)
    items.append(dict(source=str(source),path=str(destination.relative_to(ROOT)),classification=classification,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
for p in sorted(PACKET.rglob('*')):
    if p.is_file():copy(p,Path('inputs/literal-p08')/p.relative_to(PACKET),'literal recovery packet; unchanged')
for f,dst in [('p08_model.py','cakood/p08_model.py'),('test_p08_model.py','tests/test_p08_model.py'),('p08-state-contract.md','docs/recovered-p08-state-contract.md')]:
    copy(PACKET/'recovered-final'/f,dst,'literal recovered source; unchanged')
copy(P09/'source/cakood/p09_model.py','cakood/p09_model.py','literal recovered P09 dependency; unchanged')
copy(P09/'recovery-notes/manifest.json','inputs/provenance/p09-recovery-manifest.json','literal recovery manifest; unchanged')
for f,dst in [('retained_model.py','model.py'),('retained_p02_model.py','p02_model.py')]:
    copy(R/'p05-model-reconstruction/tests/fixtures'/f,'cakood/'+dst,'unchanged retained P01/P02 shared dependency')
for p in (R/'p05-scene-reconstruction/inputs/authority').glob('*.json'):
    copy(p,'inputs/authority/'+p.name,'current exact canonical authority; unchanged')
copy('/workspace/shared/cakood-context-recovery-batch2/canonical-gdd/complete-body.md','inputs/authority/complete-body.md','canonical GDD recovery; unchanged')
for stage,src,files in [
 ('p03','p03-domain-reconstruction',['p03_model.py','provenance.json','README.md','ABI.json']),
 ('p04','p04-domain-reconstruction',['model-work/p04_model.py','PROVENANCE.json','README.md','ABI.json']),
 ('p05','p05-model-reconstruction',['cakood/__init__.py','cakood/p05_model.py','cakood/composition.py','cakood/canonical-bindings.json','PROVENANCE.md','DESIGN.md']),
 ('p06','p06-model-reconstruction/revision-2',['cakood/__init__.py','cakood/p06_model.py','cakood/composition.py','cakood/canonical-bindings.json','cakood/verbal_contest.py','data/canonical-bindings.json','tests/fixtures/p08_model.py','PROVENANCE.md','API.md','REVISION-2.md']),
 ('p07','p07-model-reconstruction-r2',['cakood/__init__.py','cakood/p07_model.py','cakood/composition.py','cakood/canonical-bindings.json','PROVENANCE.md','DESIGN.md','REVISION-2.md'])]:
    for f in files:copy(R/src/f,Path('dependencies')/stage/('p04_model.py' if f=='model-work/p04_model.py' else f),'unchanged current reconstructed dependency or its provenance')
copy(R/'p07-domain-reconstruction-r2/manifest.json','inputs/current-p07-domain-manifest.json','current branch-local IDs; not historical global manifest')
(ROOT/'inputs/SOURCE-INPUTS.json').write_text(json.dumps(items,indent=2)+'\n')
print(f'Materialized {len(items)} explicit inputs; {sum(i["bytes"] for i in items)} bytes')
