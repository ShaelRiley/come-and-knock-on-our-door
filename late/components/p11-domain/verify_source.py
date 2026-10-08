"""Fail closed on changed current authority, source bindings and typed ABI."""
from pathlib import Path
import hashlib,json,re
H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify():
 from verify_inputs import verify as inputs
 count=inputs()
 m=json.loads((H/'manifest.json').read_text());source=(H/'src/module993.sc').read_text()
 methods=(H/'src/methods.sc.in').read_text()
 if source.count(methods)!=1:raise ValueError('Generated methods differ from editable source')
 expected={'source_sha256':H/'src/module993.sc','model_sha256':H/'reference/component/cakood/p11_model.py','fixture_sha256':H/'reference/component/tests/fixtures/p11/canonical-bindings.json','registry_sha256':H/'reference/component/authority/retained-registry-subset.json','authority_sha256':H/'reference/component/authority/CURRENT-SCRIPT-REVISION.json','gdd_sha256':H/'reference/component/authority/complete-body.md','accepted_pairs_sha256':H/'reference/component/authority/accepted-insult-pairs.json'}
 for key,path in expected.items():
  if m[key]!=sha(path):raise ValueError('Generated binding mismatch: '+key)
 prior=json.loads((H/'dependencies/p10-current-manifest.json').read_text())['objects']
 if {k:v for k,v in m['objects'].items() if k not in m['own_objects']}!=prior:raise ValueError('External ABI mapping mismatch')
 if m['own_objects']!={'display_wing':415,'wing_catch':416,'display_handle':417,'staging_pocket':418}:raise ValueError('P11 control allocation mismatch')
 if (m['script'],m['export'],m['standalone_species'],m['production_reserved_species'])!=(993,0,1,15):raise ValueError('P11 resource allocation mismatch')
 return dict(inputs=count,editable_methods=len(re.findall(r'\(method \(',methods)),generated_methods=len(re.findall(r'\(method \(',source)),persisted_words=len(m['persisted_properties']))
if __name__=='__main__':print(json.dumps(verify()))
