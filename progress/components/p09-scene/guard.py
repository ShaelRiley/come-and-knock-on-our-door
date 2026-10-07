"""Fail-closed frozen component input admission."""
from pathlib import Path
import hashlib,json,sys
H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,why):
 if not ok:raise RuntimeError(why)
def input_check():
 require(not sys.flags.optimize,'Optimized Python forbidden')
 files={str(p.relative_to(H)):sha(p) for p in sorted((H/'inputs').rglob('*')) if p.is_file()}
 require(files==json.loads((H/'INPUT-SEAL.json').read_text())['files'],'Frozen input inventory/hash differs')
