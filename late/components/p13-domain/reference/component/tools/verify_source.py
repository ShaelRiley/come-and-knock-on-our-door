"""NEW exact retained-method and labeled-model-delta admission, source only."""
from pathlib import Path
import hashlib,json,sys
C=Path(__file__).resolve().parents[1];W=C.parent;D=C/'stock-sci/p13-domain-adapter'
sys.path.insert(0,str(C))
from dependencies.source_tools import methods
def verify():
 original=W/'historical/literal-final/stock-sci/p13-domain-adapter'
 for name in ('codec.py','src/methods.sc.in'):
  if (D/name).read_bytes()!=(original/name).read_bytes():raise RuntimeError('Changed retained SCI/codec: '+name)
 raw=(W/'historical/literal-read/cakood/p13_model.py').read_text()
 old='or g.peg_available and not g.tested or g.peg_engaged and not (g.peg_available and g.gate_open)):'
 new='or g.peg_available and not g.tested or g.peg_engaged and not (g.peg_available and g.gate_open)\n                    # NEW current P04 owner invariant, independently contrasted.\n                    or g.wedge_in_gate and (g.peg_engaged or not g.gate_open)):'
 if raw.count(old)!=1 or (C/'cakood/p13_model.py').read_text()!=raw.replace(old,new):raise RuntimeError('Unlabeled P13 model delta')
 manifest=json.loads((D/'manifest.json').read_text())
 for field,path in [('model_sha256',C/'cakood/p13_model.py'),('fixture_sha256',C/'tests/fixtures/p13/canonical-bindings.json'),('source_sha256',D/'src/module995.sc')]:
  if hashlib.sha256(path.read_bytes()).hexdigest()!=manifest[field]:raise RuntimeError('Stale source oracle: '+field)
 expected=methods((original/'src/methods.sc.in').read_text());generated=methods((D/'src/module995.sc').read_text())
 for name,text in expected.items():
  if generated.get(name)!=text:raise RuntimeError('Retained method differs: '+name)
 objects=manifest['objects']
 for name,value in [('handcart',72),('folded_display',42),('completed_screen',81),('hotpot_pot',92)]:
  if objects[name]!=value:raise RuntimeError('Current ABI mismatch '+name)
 return dict(status='PASS',method_count=len(expected),scope='Exact retained method bodies; current context guard is generated separately; no compilation')
if __name__=='__main__':print(json.dumps(verify(),indent=2))
