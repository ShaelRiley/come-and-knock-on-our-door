"""Current P12 source, literal-method, metadata and typed allocation guards."""
from pathlib import Path
import hashlib,json,sys
H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify():
 from verify_inputs import verify as inputs
 count=inputs()
 sys.path.insert(0,str(H/'tools'))
 from source_tools import methods
 from domain_source_vm import parse
 m=json.loads((H/'manifest.json').read_text());source=(H/'src/module994.sc').read_text()
 template=(H/'src/methods.sc.in').read_text()
 if template!=(H/'historical/src/methods.sc.in').read_text():raise ValueError('Literal P12 template changed')
 if (H/'codec.py').read_bytes()!=(H/'historical/codec.py').read_bytes():raise ValueError('Retained codec changed')
 dispatch=''.join(f'(if (and (== verb 9) (== obj OBJ_{obj.upper()})) (return (self p12{method}:)))\n' for obj,method in [('swivel_release_catch','ReleaseCatch'),('rack_rotating_handle','Rotate')])
 original=methods(template.replace('; GENERATED_RACK_DISPATCH',dispatch));current=methods(source)
 if len(original)!=59:raise ValueError('Incomplete literal template')
 for name,body in original.items():
  if current.get(name)!=body:raise ValueError('Literal method changed: '+name)
 expected={'source_sha256':H/'src/module994.sc','model_sha256':H/'reference/component/cakood/p12_model.py','fixture_sha256':H/'reference/component/tests/fixtures/p12/canonical-bindings.json','registry_sha256':H/'reference/component/authority/retained-registry-subset.json','authority_sha256':H/'reference/component/authority/CURRENT-SCRIPT-REVISION.json','gdd_sha256':H/'reference/component/authority/complete-body.md','accepted_pairs_sha256':H/'reference/component/authority/accepted-insult-pairs.json','p10_abi_manifest_sha256':H/'dependencies/p10-current-manifest.json','p11_abi_manifest_sha256':H/'dependencies/p11-current-manifest.json'}
 for key,path in expected.items():
  if m[key]!=sha(path):raise ValueError('Generated binding mismatch: '+key)
 prior=json.loads((H/'dependencies/p10-current-manifest.json').read_text())['objects'];prior11=json.loads((H/'dependencies/p11-current-manifest.json').read_text())['objects']
 if {k:v for k,v in m['objects'].items() if k not in m['own_objects']}!=prior:raise ValueError('External ABI mismatch')
 if m['own_objects']!={'swivel_release_catch':419,'rack_rotating_handle':420}:raise ValueError('P12 control allocation mismatch')
 if set(m['own_objects'].values())&set(prior11.values()):raise ValueError('P12/P11 control collision')
 if any(type(v) is not int or not 1<=v<=32767 for v in m['objects'].values()) or len(set(m['objects'].values()))!=len(m['objects']):raise ValueError('Invalid typed object ABI')
 if (m['script'],m['export'],m['standalone_species'],m['production_reserved_species'])!=(994,0,1,16):raise ValueError('P12 resource allocation mismatch')
 # Reject malformed forms and ambiguous Boolean shorthand which SCI treats
 # as one expression rather than a list of conditions.
 ast=parse(source)
 cls=next(n for n in ast if n[:2]==['class','P12State'])
 forms=[n for n in cls[2:] if isinstance(n,list) and n and n[0]=='method']
 names=[n[1][0] for n in forms]
 if len(names)!=len(set(names)):raise ValueError('Duplicate methods')
 arities={n[1][0]:(n[1].index('&tmp')-1 if '&tmp' in n[1] else len(n[1])-1) for n in forms}
 sends=0;booleans=0
 def walk(n):
  nonlocal sends,booleans
  if not isinstance(n,list) or not n:return
  if n[0]=='self':
   if len(n)<2 or not isinstance(n[1],str) or not n[1].endswith(':') or n[1][:-1] not in arities or len(n)-2!=arities[n[1][:-1]]:raise ValueError('Self-send arity mismatch: '+str(n))
   sends+=1
  if n[0] in ('and','or','not'):
   booleans+=1
   if (n[0]=='not' and len(n)!=2) or (n[0] in ('and','or') and len(n)<3):raise ValueError('Boolean arity mismatch')
  if n[0] in ('==','!=','<','>','<=','>=') and len(n)!=3:raise ValueError('Comparison arity mismatch')
  if n[0]=='if':
   if len(n)<3:raise ValueError('Empty conditional body')
   for body in n[2:]:
    if isinstance(body,list) and body and body[0] in ('and','or','not','==','!=','<','>','<=','>='):raise ValueError('Bare Boolean in conditional body')
  for x in n:walk(x)
 for n in forms:walk(n)
 return dict(inputs=count,literal_methods=len(original),generated_methods=len(forms),self_sends=sends,boolean_forms=booleans,persisted_words=len(m['persisted_properties']))
if __name__=='__main__':print(json.dumps(verify()))
