"""Exact component input admission, including upstream member and compiler pins."""
from pathlib import Path
import hashlib,json,sys,stat
H=Path(__file__).resolve().parent

def require(ok,why):
 if not ok:raise RuntimeError(why)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def inventory(roots):
 result={}
 for root in roots:
  p=H/root;require(p.exists(),'Missing inventory root '+root)
  paths=[p] if p.is_file() else p.rglob('*')
  for q in sorted(paths):
   require(not q.is_symlink(),'Symlink forbidden '+str(q))
   if q.is_file():
    require('__pycache__' not in q.parts and q.suffix!='.pyc','Bytecode cache forbidden in sealed inputs')
    result[str(q.relative_to(H))]=sha(q)
 return result
EXPECTED_FROZEN_EXEC_MODES={
 'frozen-candidates/p13-scene-reconstruction/inputs/compiler-toolchain/scicompile':0o755,
 'frozen-candidates/p13-scene-reconstruction/inputs/p08/tools/scicompile':0o755,
 'frozen-candidates/p13-scene-reconstruction/tools/scicompile':0o755,
 'frozen-candidates/p14-domain-reconstruction/toolchain/scicompile':0o755,
}
def mode_inventory(roots):
 return {name:stat.S_IMODE((H/name).stat().st_mode) for name in inventory(roots)}
INPUT_ROOTS=['inputs','frozen-candidates','INPUT-CANDIDATES.json']
def input_check():
 require(not sys.flags.optimize,'Optimized Python forbidden')
 expected=json.loads((H/'INPUT-SEAL.json').read_text())
 require(expected['files']==inventory(INPUT_ROOTS),'Input inventory/hash mismatch')
 require(expected.get('modes')==mode_inventory(INPUT_ROOTS),'Input mode inventory mismatch')
 for name,mode in EXPECTED_FROZEN_EXEC_MODES.items():require(stat.S_IMODE((H/name).stat().st_mode)==mode,'Accepted dependency executable mode '+name)
 tool=H/'inputs/compiler-toolchain';manifest=json.loads((tool/'SOURCE-MANIFEST.json').read_text())['files'];actual={str(p.relative_to(tool/'source')):sha(p) for p in (tool/'source').rglob('*') if p.is_file()}
 require(actual==manifest and len(actual)==198,'Exact R2 compiler source closure')
 require(sha(H/'tools/scicompile')=='608071057b3502f4e9df530ef8c946e32d1cab8d99c809c2733928360ee49a0e','Compiler binary pin')
 require((tool/'scicompile').read_bytes()==(H/'tools/scicompile').read_bytes(),'Compiler closure executable equality')
