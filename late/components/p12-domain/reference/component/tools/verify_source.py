"""Finite SOURCE guard, not a compiler/binary/host validation claim."""
from pathlib import Path
import hashlib,json,sys
C=Path(__file__).resolve().parents[1];D=C/'stock-sci/p12-domain-adapter';W=C.parent
sys.path.insert(0,str(C))
from dependencies.source_tools import methods

def verify():
 original=W/'historical/literal-read/stock-sci/p12-domain-adapter'
 for name in ('codec.py','src/methods.sc.in'):
  if (D/name).read_bytes()!=(original/name).read_bytes():raise RuntimeError('Changed retained SCI/codec: '+name)
 manifest=json.loads((D/'manifest.json').read_text())
 for field,path in [('model_sha256',C/'cakood/p12_model.py'),('fixture_sha256',C/'tests/fixtures/p12/canonical-bindings.json'),('source_sha256',D/'src/module994.sc')]:
  if hashlib.sha256(path.read_bytes()).hexdigest()!=manifest[field]:raise RuntimeError('Stale source oracle: '+field)
 template=(original/'src/methods.sc.in').read_text()
 dispatch=''.join(f'(if (and (== verb 9) (== obj OBJ_{obj.upper()})) (return (self p12{method}:)))\n' for obj,method in [('swivel_release_catch','ReleaseCatch'),('rack_rotating_handle','Rotate')])
 expected=methods(template.replace('; GENERATED_RACK_DISPATCH',dispatch));generated=methods((D/'src/module994.sc').read_text())
 for name,text in expected.items():
  if generated.get(name)!=text:raise RuntimeError('Retained method differs: '+name)
 return dict(status='PASS_RETAINED_SOURCE_METHODS',method_count=len(expected),template_sha256=hashlib.sha256(template.encode()).hexdigest(),scope='Exact retained method bodies after original two dispatch substitutions; no compilation')
if __name__=='__main__':print(json.dumps(verify(),indent=2))
