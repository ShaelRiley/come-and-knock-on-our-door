"""NEW isolated assembly recipe. Source bytes remain literal under historical."""
from pathlib import Path
import shutil,json,hashlib
W=Path(__file__).resolve().parent;B=W.parents[1];R=B/'context-recovery-p14';A=B/'working/p13-reference-reconstruction';C=W/'component'
rows=[]
def cp(src,dst,pin=True):
 p=W/dst;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,p);raw=p.read_bytes()
 rows.append(dict(source=str(src.relative_to(B)),target=dst,pinned=pin,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
for folder in ('literal-original','literal-final','literal-read','literal-read-partial','literal-derived','recorded-edits','packets','dependencies'):
 for p in sorted((R/folder).rglob('*')):
  if p.is_file():cp(p,'historical/'+str(p.relative_to(R)))
for n in ('SOURCE-COMPLETENESS.json','RECOVERY.md','RECOVERY-STATUS.json','transcription-manifest.json','historical-anchors.json'):
 cp(R/n,'historical/'+n)
for folder in ('cakood','dependencies','authority'):
 for p in sorted((A/'component'/folder).rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts:cp(p,'component/'+str(p.relative_to(A/'component')),p.name!='verbal_contest.py' or 'vc_owner' in p.parts)
for n in ('test_verbal_contest.py','current_join.py'):
 cp(A/'component/tests'/n,'component/tests/'+n)
cp(A/'component/tools/assertions.py','component/tools/assertions.py')
cp(A/'component/tools/verify_inputs.py','component/tools/verify_inputs.py',False)
cp(A/'component/cakood/verbal_contest.py','historical/accepted-p13/verbal_contest.py')
cp(A/'component/tests/test_late_campaign_models.py','historical/accepted-p13/test_late_campaign_models.py')
for n in ('README.md','STATUS.json','provenance/input-inventory.json','provenance/working-differences.json'):
 cp(A/n,'historical/accepted-p13/'+n)
cp(B/'context-recovery-p13/literal-read-partial/tests/test_late_campaign_models.py.lines1-85.part','historical/partial-late-campaign/lines1-85.part')
cp(R/'literal-read/cakood/p14_model.py','component/cakood/p14_model.py')
cp(R/'literal-read/docs/p14-state-contract.md','component/docs/p14-state-contract.md')
for p in sorted((R/'literal-final/stock-sci/p14-domain-adapter').rglob('*')):
 if p.is_file():cp(p,'component/stock-sci/p14-domain-adapter/'+str(p.relative_to(R/'literal-final/stock-sci/p14-domain-adapter')),p.name in ('codec.py','methods.sc.in'))
cp(A/'component/stock-sci/p13-domain-adapter/manifest.json','component/dependencies/p13-current-manifest.json')
for n in ('SELECTOR-CAPACITY-20261007.json','P13-P14-CANONICAL-IDENTITY-PREFLIGHT.json'):
 cp(B/'integration-planning'/n,'provenance/'+n)
(W/'provenance/input-inventory.json').write_text(json.dumps(rows,indent=2)+'\n')
(W/'evidence').mkdir(exist_ok=True)
print('Frozen files:',len(rows))
