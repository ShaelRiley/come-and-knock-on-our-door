"""Editable, fail-closed source/input/output and evidence boundary."""
from pathlib import Path
import sys,json,subprocess,zipfile,os,stat
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
from guard import require,sha,inventory,input_check,INPUT_ROOTS,mode_inventory

def dump(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2)+'\n')
def source_files():
 roots=[p.name for p in H.iterdir() if p.is_file() and (p.suffix=='.py' or p.name in ('README.md','PROVENANCE.md','COMPATIBILITY.json'))]+['tools','tests']
 return inventory(roots)
def source_check():
 input_check();s=json.loads((H/'SOURCE-SEAL.json').read_text());require(s['files']==source_files(),'Source inventory/hash mismatch');require(s.get('modes')=={n:stat.S_IMODE((H/n).stat().st_mode) for n in s['files']},'Source mode inventory mismatch');require(s['input_seal_sha256']==sha(H/'INPUT-SEAL.json'),'Source sealed against different inputs')
def output_files():return inventory(['generated','build'])
def output_check():
 source_check();o=json.loads((H/'OUTPUT-SEAL.json').read_text());require(o['files']==output_files(),'Output inventory/hash mismatch');require(o['source_seal_sha256']==sha(H/'SOURCE-SEAL.json'),'Stale output source binding')
 t=json.loads((H/'evidence/tests.json').read_text());require(t['status']=='PASS' and t['source_seal_sha256']==sha(H/'SOURCE-SEAL.json') and t['ids']==json.loads((H/'tests/EXPECTED-TESTS.json').read_text()),'Stale/incomplete tests')
 for name in ('audio-verification.json','emission-audit.json'):require(json.loads((H/'evidence'/name).read_text())['status'].startswith('PASS'),'Required gate '+name)
 for i in range(8):require(json.loads((H/f'evidence/date-matrix-{i}.json').read_text())['selected_synthetic_lengths']==list(range(i*10+1,i*10+11)),'Date matrix coverage')
def state(status,**kw):dump(H/'VERIFICATION.json',dict(status=status,native_acceptance=False,production_host_acceptance=False,**kw))
def command(args,log):
 p=subprocess.run([sys.executable,'-B',*[str(a) for a in args]],cwd=H,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});(H/'evidence'/log).write_text(p.stdout+p.stderr);require(p.returncode==0,'Failed '+str(args)+'; see '+log)
def rebuild():
 source_check();(H/'evidence').mkdir(exist_ok=True);state('REBUILD_RUNNING')
 for script,log in [('generate.py','generation.log'),('font.py','font.log'),('extend_dialogue.py','extension.log'),('build.py','build.log'),('verify_audio.py','audio-verification.log'),('tests/run_suite.py','tests.log'),('tools/audit_emission.py','emission-audit.log'),('render_font_review.py','font-review.log'),('render_panels.py','font-panels.log')]:command([H/script],log)
 for i in range(8):command([H/'tests/date_matrix.py',i],f'date-matrix-{i}.log')
 source_check();dump(H/'OUTPUT-SEAL.json',dict(source_seal_sha256=sha(H/'SOURCE-SEAL.json'),files=output_files()));output_check();state('PASS_SOURCE_COMPONENT_CANDIDATE',source_seal_sha256=sha(H/'SOURCE-SEAL.json'),output_seal_sha256=sha(H/'OUTPUT-SEAL.json'))
GATES=['evidence/R1-MODE-ADMISSION.json','evidence/R1-CONTENT-DELTA.json','evidence/R1-CALLE-QUALIFICATION.json','evidence/compile-proof.json','evidence/font1-glyph-contact-sheet.png','evidence/font1-url-date-examples.png','evidence/font1-exact-panel-leading.png','evidence/tests.json','evidence/audio-verification.json','evidence/emission-audit.json','evidence/font-coverage.json','evidence/font-panel-pixels.json','evidence/cold-rebuild.json','evidence/negative-checks.json']+[f'evidence/date-matrix-{i}.json' for i in range(8)]
def gate_check():
 g=json.loads((H/'GATE-SEAL.json').read_text());require(g.get('source_seal_sha256')==sha(H/'SOURCE-SEAL.json') and g.get('output_seal_sha256')==sha(H/'OUTPUT-SEAL.json'),'Stale gate source/output binding');require(g.get('files')=={n:sha(H/n) for n in GATES},'Gate inventory/hash mismatch')
def package():
 output_check();gate_check();require(json.loads((H/'evidence/cold-rebuild.json').read_text())['status']=='PASS','Cold rebuild required');require(json.loads((H/'evidence/negative-checks.json').read_text())['status']=='PASS','Admission negatives required')
 for file in ('evidence/cold-rebuild.json','evidence/negative-checks.json'):
  r=json.loads((H/file).read_text());require(r['source_seal_sha256']==sha(H/'SOURCE-SEAL.json') and r['output_seal_sha256']==sha(H/'OUTPUT-SEAL.json'),'Stale final gate '+file)
 (H/'delivery').mkdir(exist_ok=True);out=H/'delivery/P14-Scene-Editable-Component-20261007.zip';paths=set()
 for root in [*INPUT_ROOTS,'tools','tests','generated','build','evidence']:
  p=H/root
  for q in ([p] if p.is_file() else p.rglob('*')):
   if q.is_file():paths.add(q)
 for q in H.iterdir():
  if q.is_file() and (q.suffix=='.py' or q.name in ('README.md','PROVENANCE.md','COMPATIBILITY.json','INPUT-SEAL.json','SOURCE-SEAL.json','OUTPUT-SEAL.json','GATE-SEAL.json','VERIFICATION.json')):paths.add(q)
 members={str(p.relative_to(H)):sha(p) for p in sorted(paths)};dump(H/'PACKAGE-MANIFEST.json',dict(files=members,member_modes={str(p.relative_to(H)):stat.S_IMODE(p.stat().st_mode) for p in sorted(paths)},manifest_mode=0o644,archive_root='p14-scene-reconstruction',status='SEALED_SOURCE_CANDIDATE_NOT_INDEPENDENT_ACCEPTANCE'));paths.add(H/'PACKAGE-MANIFEST.json')
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in sorted(paths):z.write(p,'p14-scene-reconstruction/'+str(p.relative_to(H)))
 output_check();dump(H/'delivery/FINAL-ARTIFACT.json',dict(path=str(out),bytes=out.stat().st_size,sha256=sha(out),members=len(paths)));print(out,out.stat().st_size,sha(out))
if __name__=='__main__':
 try:
  require(not sys.flags.optimize,'Optimized Python forbidden');mode=sys.argv[1] if len(sys.argv)>1 else 'verify'
  if mode=='seal-input':dump(H/'INPUT-SEAL.json',dict(files=inventory(INPUT_ROOTS),modes=mode_inventory(INPUT_ROOTS)))
  elif mode=='seal-source':input_check();dump(H/'SOURCE-SEAL.json',dict(input_seal_sha256=sha(H/'INPUT-SEAL.json'),files=source_files(),modes={n:stat.S_IMODE((H/n).stat().st_mode) for n in source_files()}));state('SOURCE_SEALED_NOT_VERIFIED')
  elif mode=='rebuild':rebuild()
  elif mode=='verify':
   output_check()
   if (H/'GATE-SEAL.json').exists():gate_check()
   state('PASS_SOURCE_COMPONENT_CANDIDATE',source_seal_sha256=sha(H/'SOURCE-SEAL.json'),output_seal_sha256=sha(H/'OUTPUT-SEAL.json'));print('PASS sealed component')
  elif mode=='seal-gates':output_check();dump(H/'GATE-SEAL.json',dict(source_seal_sha256=sha(H/'SOURCE-SEAL.json'),output_seal_sha256=sha(H/'OUTPUT-SEAL.json'),files={n:sha(H/n) for n in GATES}));gate_check()
  elif mode=='package':package()
  else:raise ValueError('Unknown mode')
 except Exception as e:state('FAILED',reason=str(e));raise
