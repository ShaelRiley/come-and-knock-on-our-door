#!/usr/bin/env python3
"""Fresh coherent fixture source compile. No emitted resource is a compiler input."""
from pathlib import Path
import json,hashlib,sys,shutil,subprocess
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'tools'))
import pack
from extract_sci11 import extract

def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 need(not sys.flags.optimize,'optimized Python forbidden')
 E=H/'evidence';E.mkdir(exist_ok=True);B=H/'build/fresh'
 if B.exists():shutil.rmtree(B)
 (B/'src').mkdir(parents=True);(B/'compiled').mkdir()
 compiler=H/'toolchain/scicompile';need(sha(compiler)=='608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e','compiler hash');compiler.chmod(0o755)
 (B/'src/main.sc').write_text((H/'inputs/original981/main-fixture.sc').read_text()+'\n(instance responsiveSound of Sound (properties number 151 loop -1 priority 100 vol 0))\n')
 for number,source in [(981,H/'inputs/original981/score.sc'),(986,H/'inputs/domain/module986.sc'),(940,H/'inputs/accepted-v4/generated/module940.sc')]+[(n,H/f'generated/module{n}.sc')for n in (941,942,943)]:
  (B/f'src/module{number}.sc').write_bytes(source.read_bytes())
 order=[0,981,986,940,941,942,943]
 (B/'game.ini').write_text('[Game]\nName=Responsive music isolated source fixture\nLanguage=sci\n[Script]\nn000=main\n'+''.join(f'n{n}=module{n}\n'for n in order[1:]))
 pack.pack_resources({(6,n):(H/f'inputs/host-{n}.vocab.bin').read_bytes()for n in(996,997)},B)
 (B/'selector-list.json').write_bytes((H/'inputs/host-selectors.json').read_bytes())
 receipts=[];layouts={}
 for n in order:
  source=B/f'src/{"main"if n==0 else "module"+str(n)}.sc';target=B/f'compiled/{n}.scr.bin'
  p=subprocess.run([str(compiler),'--version','sci11',str(B),str(source),str(target)],capture_output=True,text=True)
  (E/f'compile-{n}.log').write_text(p.stdout+p.stderr);need(p.returncode==0 and '[error]'not in p.stdout+p.stderr,p.stdout+p.stderr)
  layouts[str(n)]=extract(target,Path(str(target)+'.hep'),H/'inputs/host-selectors.json')
  receipts.append(dict(module=n,script_sha256=sha(target),heap_sha256=sha(Path(str(target)+'.hep')),source_sha256=sha(source),script_bytes=target.stat().st_size,heap_bytes=Path(str(target)+'.hep').stat().st_size))
  print(n,receipts[-1]['script_bytes'],receipts[-1]['heap_bytes'],flush=True)
 old=json.loads((H/'inputs/original981/layout.json').read_text())
 need(layouts['981']['script_sha256']==old['script_sha256']and layouts['981']['heap_sha256']==old['heap_sha256'],'original981 changed')
 for n in(941,942):
  objs=layouts[str(n)]['objects'];need(len(objs)==1 and not objs[0]['is_class']and objs[0]['superclass']==3 and len(objs[0]['methods'])==43,'transport class/API altered')
 need(not layouts['943']['objects'],'broker unexpectedly created object/class')
 for row in receipts:need(row['script_bytes']+row['heap_bytes']+2<65536,'SCI segment budget')
 (B/'compile-receipt.json').write_text(json.dumps(dict(status='PASS_FRESH_COMPILE',modules=receipts),indent=2)+'\n')
 (E/'layouts.json').write_text(json.dumps(layouts,indent=2)+'\n')
if __name__=='__main__':main()
