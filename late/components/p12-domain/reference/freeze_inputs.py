from pathlib import Path
import shutil,json,hashlib,zipfile
W=Path(__file__).resolve().parent; B=W.parents[1]
R=B/'context-recovery-p13'; P11=B/'working/p11-reference-recovery/revisions/review02/component'
V=B/'reviews/p08-r2-bounded-20261006-2318/p08-r2-reconstructed/fixtures/reference-baseline/dependencies/p06'
entries=[]
def copy(src,dest):
 dest=W/dest;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
 b=dest.read_bytes();entries.append(dict(source=str(src.relative_to(B)),target=str(dest.relative_to(W)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
for name in ('SOURCE-COMPLETENESS.json','transcription-manifest.json','RECOVERY.md'):
 copy(R/name,'historical/'+name)
for folder in ('literal-read','literal-read-partial','packets','recorded-edits'):
 for src in (R/folder).rglob('*'):
  if src.is_file() and ('p12' in str(src.relative_to(R)).lower() or 'late-campaign' in src.name or 'late_campaign' in src.name or src.name=='p13_model.py' or src.name=='p13-state-contract.md'):
   copy(src,'historical/'+str(src.relative_to(R)))
for name in ('__init__.py','model.py','p02_model.py','p03_model.py','p04_model.py','p09_model.py','p10_model.py','p11_model.py'):
 copy(P11/'cakood'/name,'component/cakood/'+name)
for src in (P11/'dependencies').glob('*'):
 if src.is_file():copy(src,'component/dependencies/'+src.name)
for src in (B/'canonical-authority').glob('*'):
 if src.is_file():copy(src,'component/authority/'+src.name)
copy(R/'literal-read/cakood/p13_model.py','component/cakood/p13_model.py')
copy(V/'cakood/verbal_contest.py','component/dependencies/vc_owner/verbal_contest.py')
copy(V/'data/canonical-bindings.json','component/dependencies/data/canonical-bindings.json')
copy(B/'working/p10-domain-reconstruction/manifest.json','component/dependencies/p10-current-manifest.json')
copy(B/'working/p10-domain-reconstruction/tools/domain_source_vm.py','component/dependencies/domain_source_vm.py')
copy(B/'working/p10-domain-reconstruction/tools/p06_domain_source_vm.py','component/dependencies/p06_domain_source_vm.py')
copy(B/'working/p10-domain-reconstruction/tools/source_tools.py','component/dependencies/source_tools.py')
for name in ('test_p11_model.py','test_current_contract.py','test_f01_sincere_listener.py'):
 copy(P11/'tests'/name,'component/tests/dependency_'+name)
(W/'component/dependencies/vc_owner/__init__.py').write_text('')
(W/'component/cakood/p12_model.py').write_bytes((R/'literal-read-partial/cakood/p12_model.py.part').read_bytes())
(W/'provenance').mkdir(exist_ok=True)
(W/'provenance/input-inventory.json').write_text(json.dumps(entries,indent=2)+'\n')
(W/'STATUS.json').write_text(json.dumps(dict(status='EARLY_INPUT_CHECKPOINT',recovered_prefix_bytes=11306,missing='All P12World methods after _block; reconstruction pending',scope='Finite reference-model reconstruction; no native or SCI compilation acceptance'),indent=2)+'\n')
(W/'checkpoints').mkdir(exist_ok=True)
with zipfile.ZipFile(W/'checkpoints/P12-Reference-Reconstruction-Checkpoint.zip','w',zipfile.ZIP_DEFLATED) as z:
 for path in sorted(W.rglob('*')):
  if path.is_file() and 'checkpoints' not in path.parts:z.write(path,'p12-reference-reconstruction/'+str(path.relative_to(W)))
print(len(entries),'input files frozen')
