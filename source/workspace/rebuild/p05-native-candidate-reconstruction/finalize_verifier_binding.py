#!/usr/bin/env python3
"""Bind an outer-verifier-only correction to an unchanged completed game/test run.

No full test rerun is claimed. The old full receipt, all proofs and exact input
identities remain immutable evidence; independent negative bootstrap probes bind
the changed verifier. Every game/data/test/dependency identity must stay exact.
"""
from pathlib import Path
import json,hashlib,shutil,subprocess,sys,ast
N=Path(__file__).resolve().parent;R=N.parent;H=R/'p05-host-reconstruction';P=R/'p05-host-verifier-membership-review';A=H/'evidence/final-primary-run';OUT=H/'VERIFICATION.json'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def require(ok,message):
 if not ok:raise RuntimeError(message)
def dump(p,value):Path(p).write_text(json.dumps(value,indent=2)+'\n')
require(not sys.flags.optimize,'Optimized binding forbidden')
require(not A.exists(),'Primary full-run archive already exists; do not rewrite it')
old=json.loads(OUT.read_text());require(old['status']=='PASS_SOURCE_EMITTED_STATIC_ONLY','Primary full suite has not passed')
require(sha(H/'INPUTS.json')==old['input_manifest_sha256']=='e2733548f91628a2cb24e97ded62a45ff1c9a8622347fbfb842f9e68ad4dc006','Unexpected tested input seal')
original=json.loads((H/'INPUTS.json').read_text());suite=json.loads((H/'evidence/suite.json').read_text())
require(suite['status']=='PASS' and suite['tests']==44 and not suite['skipped'] and not suite['failures'] and not suite['errors'],'Complete44-test result required')
A.mkdir(parents=True)
files=['INPUTS.json','VERIFICATION.json','verify.py','build/coherent/compile-receipt.json','tests/EXPECTED-TESTS.json',*old['proofs'].keys(),'evidence/verify-run_suite.log','evidence/verify-console.log']
for file in files:
 p=H/file;q=A/file;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);require(sha(p)==sha(q),'Full-run archive copy differs')
for file,digest in old['proofs'].items():require(sha(A/file)==digest,'Primary proof identity changed')
dump(OUT,{'status':'REBINDING_OUTER_VERIFIER_ONLY','native_acceptance':False})
try:
 expected_verifier='fe59417685a6fa1ae5a2dda9b95cc3b78d8b2c4564cf76e09a663050ebc1edc4';expected_membership='1b52926ecae901c09d751dad2b79850b403adc48d44e199569395138a9e513fa'
 require(sha(P/'verify.py')==expected_verifier and sha(P/'EXPECTED-INPUT-PATHS.json')==expected_membership,'Corrected verifier identity changed')
 for file in ['verify.py','EXPECTED-INPUT-PATHS.json']:shutil.copy2(P/file,H/file)
 subprocess.run([sys.executable,str(H/'tools/seal_inputs.py')],check=True)
 current=json.loads((H/'INPUTS.json').read_text());seal=sha(H/'INPUTS.json')
 require(seal=='3702d7501adb5602f8daff63873eea7e516fe564c7f567170a646c51b2ffb0e2','Corrected seal differs from independent reviewer')
 require(current['external']==original['external'],'Retained dependency drift')
 added=set(current['local'])-set(original['local']);removed=set(original['local'])-set(current['local']);changed={name for name in set(current['local'])&set(original['local']) if current['local'][name]!=original['local'][name]}
 require(added=={'EXPECTED-INPUT-PATHS.json'} and not removed and changed=={'verify.py'},'Game/data/test input drift')
 # Execute the exact corrected inventory predicates, without claiming another
 # full public build/test run. Full bootstrap failures were independently probed.
 tree=ast.parse((H/'verify.py').read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('require','inventory')];require(len(defs)==2,'Corrected inventory function shape')
 env={'H':H,'R':R,'json':json,'Path':Path,'sha':sha};exec(compile(ast.Module(body=defs,type_ignores=[]),str(H/'verify.py'),'exec'),env);env['inventory']()
 sys.path.insert(0,str(H/'tools'));from validate_selected_inputs import check
 check(H)
 guard=R/'p05-host-independent-review/verifier-probe-results/RESULT.json';g=json.loads(guard.read_text())
 require(g['status']=='PASS_FAIL_CLOSED_VERIFIER_PROBES' and g['verifier_sha256']==expected_verifier and g['membership_sha256']==expected_membership,'Independent verifier failure probes not bound')
 shutil.copy2(guard,H/'evidence/verifier-guard-probes.json')
 for row in old['compiled_modules']:
  n=row['module'];require(sha(H/'src'/('main.sc' if n==0 else f'module{n}.sc'))==row['source_sha256'],'Game source drift')
  for part,suffix in [('script',''),('heap','.hep')]:require(sha(H/f'build/coherent/compiled/{n}.scr.bin{suffix}')==row[part+'_sha256'],'Game emitted-byte drift')
 correction={'status':'PASS_OUTER_VERIFIER_ONLY_BINDING','defect':'The old inventory checker accepted a schema1 manifest with empty/truncated local or external dictionaries, hashing only supplied members.','fix':'Literal-pinned expected membership identity plus exact local/external path sets and strict integer schema before per-file hashing.','old_input_manifest_sha256':old['input_manifest_sha256'],'new_input_manifest_sha256':seal,'old_verifier_sha256':sha(A/'verify.py'),'new_verifier_sha256':expected_verifier,'new_membership_sha256':expected_membership,'unchanged_local_game_data_test_inputs':len(original['local'])-1,'unchanged_external_inputs':len(original['external']),'added':sorted(added),'changed':sorted(changed),'removed':sorted(removed),'primary_full_run_receipt_sha256':sha(A/'VERIFICATION.json'),'primary_full_run_tests':44,'primary_full_run_skips':0,'independent_guard_receipt_sha256':sha(guard),'positive_check':'Exact corrected inventory() function and canonical input validators passed','full_test_rerun_claimed':False,'native_acceptance':False}
 dump(H/'evidence/verifier-correction.json',correction)
 final=dict(old);final.update(input_manifest_sha256=seal,verification_method='Hash-bound split evidence: completed unchanged game/data/test run plus corrected outer-verifier inventory and independent failure probes',original_full_test_input_manifest_sha256=old['input_manifest_sha256'],full_test_rerun_claimed=False)
 final['proofs']=dict(old['proofs']);final['proofs']['evidence/verifier-correction.json']=sha(H/'evidence/verifier-correction.json');final['proofs']['evidence/verifier-guard-probes.json']=sha(H/'evidence/verifier-guard-probes.json')
 dump(OUT,final);print(json.dumps(correction,indent=2))
except BaseException as e:
 dump(OUT,{'status':'FAIL','error':str(e),'native_acceptance':False});raise
