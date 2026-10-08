"""Cold own-source rebuild with exact accepted dependencies, in a path with spaces."""
from pathlib import Path
import json,sys,shutil,subprocess
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
from guard import require,sha
import run

def main():
 run.output_check();dest=H/'portability/cold source only/P14 component';require(not dest.exists(),'Fresh cold destination required')
 inputs=json.loads((H/'INPUT-SEAL.json').read_text())['files'];source=json.loads((H/'SOURCE-SEAL.json').read_text())['files'];files=set(inputs)|set(source)|{'INPUT-SEAL.json','SOURCE-SEAL.json'}
 for name in sorted(files):
  target=dest/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(H/name,target)
 require(not (dest/'generated').exists() and not (dest/'build').exists(),'Own generated outputs must not be copied')
 result=subprocess.run([sys.executable,'-B',str(dest/'run.py'),'rebuild'],cwd=dest,capture_output=True,text=True);(H/'evidence/cold-rebuild.log').write_text(result.stdout+result.stderr);require(result.returncode==0,'Cold rebuild failed; inspect cold evidence logs')
 expected=json.loads((H/'OUTPUT-SEAL.json').read_text())['files'];actual=json.loads((dest/'OUTPUT-SEAL.json').read_text())['files'];require(actual==expected,'Cold exact output inventory/byte mismatch')
 for name in ('font1-glyph-contact-sheet.png','font1-url-date-examples.png','font1-exact-panel-leading.png'):require(sha(H/'evidence'/name)==sha(dest/'evidence'/name),'Cold font pixel matrix mismatch '+name)
 r=dict(status='PASS',clean_own_source_only_rebuild=True,accepted_emitted_domain_dependency_retained=True,own_generated_output_files=len(expected),exact_every_output_byte=True,tests=json.loads((dest/'evidence/tests.json').read_text())['tests'],date_lengths=80,source_seal_sha256=sha(H/'SOURCE-SEAL.json'),output_seal_sha256=sha(H/'OUTPUT-SEAL.json'),native_acceptance=False)
 (H/'evidence/cold-rebuild.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
if __name__=='__main__':main()
