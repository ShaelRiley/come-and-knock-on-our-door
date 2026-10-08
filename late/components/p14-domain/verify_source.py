"""NEW current reference identity, literal preservation and finite SCI guards."""
from pathlib import Path
import hashlib,json,sys
H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify():
 from verify_inputs import verify as inputs
 count=inputs()
 sys.path.insert(0,str(H/'tools'))
 from source_tools import methods
 m=json.loads((H/'manifest.json').read_text());source=(H/'src/module996.sc').read_text()
 reference=H/'reference/component/stock-sci/p14-domain-adapter'
 for name in ('src/module996.sc','manifest.json','codec.py','src/methods.sc.in','object-bindings.json'):
  if (H/name).read_bytes()!=(reference/name).read_bytes():raise ValueError('Accepted current source/schema mismatch: '+name)
 for name in ('codec.py','src/methods.sc.in'):
  if (H/name).read_bytes()!=(H/'historical/adapter'/name).read_bytes():raise ValueError('Literal source changed: '+name)
 original=methods((H/'src/methods.sc.in').read_text());current=methods(source)
 if len(original)!=77:raise ValueError('Incomplete literal template')
 for name,body in original.items():
  if current.get(name)!=body:raise ValueError('Literal method changed: '+name)
 C=H/'reference/component'
 expected={'source_sha256':H/'src/module996.sc','model_sha256':C/'cakood/p14_model.py','fixture_sha256':C/'tests/fixtures/p14/canonical-bindings.json','registry_sha256':C/'authority/retained-registry-subset.json','authority_sha256':C/'authority/CURRENT-SCRIPT-REVISION.json','gdd_sha256':C/'authority/complete-body.md'}
 for key,path in expected.items():
  if m[key]!=sha(path):raise ValueError('Generated binding mismatch: '+key)
 for name,digest in [('full-line-catalog.json','3c6a8dc5a4afacd9704a79f84044d6dad623aa596df9e7638c8dff29e607150c'),('speech-units.json','d143242b3d56f57331b0adfb73481425792c0757f57bc0c01a1b94561527c475')]:
  if sha(C/'authority'/name)!=digest:raise ValueError('Current canonical authority mismatch')
 prior=json.loads((C/'dependencies/p13-current-manifest.json').read_text())['objects']
 if {k:v for k,v in m['objects'].items() if k not in m['own_objects']}!=prior:raise ValueError('External ABI mismatch')
 if list(m['own_objects'].values())!=list(range(435,443)) or set(m['own_objects'].values())&set(prior.values()):raise ValueError('Local card allocation mismatch')
 if (len(m['all_properties']),len(m['persisted_properties']),len(m['serials']))!=(669,642,202):raise ValueError('Finite layout changed')
 if (m['script'],m['export'],m['standalone_species'],m['production_reserved_species'])!=(996,0,1,18):raise ValueError('P14 allocation mismatch')
 result=syntax(source)
 return dict(inputs=count,literal_methods=77,persisted_words=642,**result)
def syntax(source):
 sys.path.insert(0,str(H/'tools'))
 from domain_source_vm import parse
 # Reject malformed forms and ambiguous Boolean shorthand which SCI treats
 # as one expression rather than a list of conditions.
 ast=parse(source)
 cls=next(n for n in ast if n[:2]==['class','P14State'])
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
 return dict(generated_methods=len(forms),self_sends=sends,boolean_forms=booleans)
if __name__=='__main__':print(json.dumps(verify()))
