"""NEW finite P13 candidate input closure. Run only in this isolated packet."""
from pathlib import Path
import shutil, json, hashlib, zipfile
W=Path(__file__).resolve().parent; B=W.parents[1]
R=B/'context-recovery-p13'; P12=B/'working/p12-reference-reconstruction/component'
P8=B/'reviews/p08-r2-bounded-20261006-2318/p08-r2-reconstructed/fixtures/reference-baseline'
rows=[]
def copy(src,relative,pinned=True):
 d=W/relative;d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,d)
 raw=d.read_bytes();rows.append(dict(source=str(src.relative_to(B)),target=relative,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pinned=pinned))
for folder in ('literal-original','literal-final','literal-read','literal-read-partial','literal-derived','recorded-edits','packets'):
 for p in sorted((R/folder).rglob('*')):
  if p.is_file():copy(p,'historical/'+str(p.relative_to(R)))
for name in ('SOURCE-COMPLETENESS.json','transcription-manifest.json','RECOVERY.md','RECOVERY-STATUS.json'):
 copy(R/name,'historical/'+name)
for folder in ('cakood','dependencies','authority'):
 for p in sorted((P12/folder).rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts:copy(p,'component/'+str(p.relative_to(P12)),p.name!='p13_model.py')
copy(P12/'tools/assertions.py','component/tools/assertions.py')
copy(P12/'tests/test_verbal_contest.py','component/tests/test_verbal_contest.py')
copy(P12/'tests/test_p12_current.py','historical/accepted-p12/test_p12_current.py')
copy(P8/'cakood/p08_model.py','component/cakood/p08_model.py')
for p in sorted((P8/'dependencies/p07').rglob('*')):
 if p.is_file() and '__pycache__' not in p.parts:copy(p,'component/dependencies/p07_owner/'+str(p.relative_to(P8/'dependencies/p07')))
for n in ('manifest.json','layout.json','module988.sc','ABI.md','HOST-CONTRACT.md'):
 copy(B/'extracted/p07-source/snapshot/domain'/n,'component/dependencies/p07-current-domain/'+n)
copy(B/'working/p11-domain-reconstruction/manifest.json','component/dependencies/p11-current-manifest.json')
for p in sorted((R/'literal-final/stock-sci/p13-domain-adapter').rglob('*')):
 if p.is_file():copy(p,'component/stock-sci/p13-domain-adapter/'+str(p.relative_to(R/'literal-final/stock-sci/p13-domain-adapter')),False)
for n in ('P13-RECOVERY-NEXT-GATE.json','integration-planning/P13-P14-CANONICAL-IDENTITY-PREFLIGHT.json'):
 copy(B/n,'provenance/'+Path(n).name)
(W/'provenance/input-inventory.json').write_text(json.dumps(rows,indent=2)+'\n')
(W/'evidence').mkdir(exist_ok=True)
(W/'STATUS.json').write_text(json.dumps({'status':'INPUTS_FROZEN','scope':'P13 finite reference/source candidate; no compilation, host or native acceptance','original_model_sha256':'0cd474faba3820d7a5b30be7fc7f78131141d9866e0288b10a8704fe02553eb5'},indent=2)+'\n')
print(len(rows),'source inputs frozen')
