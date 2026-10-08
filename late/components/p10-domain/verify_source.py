"""Validate the generated adapter's authority and immutable method closure."""
from pathlib import Path
import hashlib,json,re
H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify():
    from verify_inputs import verify as inputs
    count=inputs()
    m=json.loads((H/'manifest.json').read_text());source=(H/'src/module992.sc').read_text()
    literal=(H/'historical/literal/src/methods.sc.in.txt').read_bytes()
    if (H/'src/methods.sc.in').read_bytes()!=literal:raise ValueError('Literal methods changed without an adaptation gate')
    if source.count(literal.decode())!=1:raise ValueError('Generated source does not contain exact method closure')
    if len(re.findall(r'\(method \(',literal.decode()))!=56:raise ValueError('Incomplete literal method count')
    expected={'source_sha256':H/'src/module992.sc','model_sha256':H/'reference/cakood/p10_model.py',
      'fixture_sha256':H/'reference/tests/fixtures/p10/canonical-bindings.json',
      'registry_sha256':H/'reference/authority/retained-registry-subset.json',
      'authority_sha256':H/'reference/authority/CURRENT-SCRIPT-REVISION.json','gdd_sha256':H/'reference/authority/complete-body.md'}
    for key,path in expected.items():
        if m[key]!=sha(path):raise ValueError('Generated source binding mismatch: '+key)
    prior=json.loads((H/'dependencies/p09-current-schema.json').read_text())['objects']
    if {k:v for k,v in m['objects'].items() if k not in m['own_objects']}!=prior:
        raise ValueError('Current external object mapping differs')
    if m['own_objects']!={'cue_rack':410,'rack_spring_clips':411,'master_invitation_cue_1':412,'master_invitation_cue_2':413,'master_invitation_cue_3':414}:
        raise ValueError('P10 allocation changed')
    return dict(inputs=count,literal_methods=56,generated_methods=len(re.findall(r'\(method \(',source)),persisted_words=len(m['persisted_properties']))
if __name__=='__main__':print(json.dumps(verify()))
