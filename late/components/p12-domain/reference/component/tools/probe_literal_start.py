"""Reproduce a defect in the recovered start METHOD, not a lost full model."""
from pathlib import Path
import sys,json
from dataclasses import replace
CROOT=Path(__file__).resolve().parents[1];D=CROOT/'stock-sci/p12-domain-adapter';sys.path[:0]=[str(CROOT),str(CROOT/'tests'),str(D),str(D/'tests')]
from test_domain import C,RACK,Harness,P12World,COURTYARD,TILE_IDS,M
c=replace(C,inventory=frozenset({'cue_rack'}))
w=P12World();before=w.save();historical_method_result=w._literal_start(c,RACK)
h=Harness();h.project(c);h.v.call('p12Handoff',M['objects']['cue_rack'],M['rooms'][COURTYARD],0,1,*[M['objects'][x] for x in TILE_IDS],1,2,3)
if historical_method_result.code!='rack_rehung' or h.v.p['p12Code']!=M['codes']['invalid_context']:raise RuntimeError('Expected comparison no longer reproduces')
new=P12World();error=None
try:new.start(c,RACK)
except ValueError as exc:error=str(exc)
if error is None or new.save()!=before:raise RuntimeError('Correction did not reject without mutation')
result=dict(status='EXPECTED_ORIGINAL_METHOD_DEFECT_REPRODUCED_AND_CORRECTION_PASS',literal_method='P12World.start, recovered lines265-283, executed as _literal_start on new reconstructed class',not_claimed='No missing historical full-model execution',input='Actual cue rack incorrectly held in external inventory at first handoff',recovered_method_code=historical_method_result.code,retained_sci_code='invalid_context',new_wrapper_error=error,new_state_unchanged=True,regression_test='CurrentTests.test_literal_start_defect_contrast_and_corrected_repeat_semantics')
print(json.dumps(result,indent=2))
