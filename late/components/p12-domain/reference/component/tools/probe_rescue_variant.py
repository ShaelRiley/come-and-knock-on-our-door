"""Explicit contrast for the pre-engaged result-caption fixture bridge."""
from pathlib import Path
import sys,json
C=Path(__file__).resolve().parents[1];D=C/'stock-sci/p12-domain-adapter';sys.path[:0]=[str(C),str(C/'tests'),str(D),str(D/'tests')]
from test_p12_current import genuine_upstream
p3,p4,p9,p10,p11,vc,c,shown=genuine_upstream(preengaged=True)
p=next(p for p in shown if p.unit_id=='VC03.LOSS.02')
unit=vc.catalog.speech_unit(p.unit_id);expected=next(v for v in unit['finite_variants'] if v['variant_id']=='pre_engaged')['text']
if unit['text']==expected or p.text!=expected:raise RuntimeError('Variant contrast not established')
print(json.dumps(dict(status='EXPECTED_BASE_WORDING_MISMATCH_AND_CORRECTED_READ_RECEIPT',scope='Test-only host presentation selection; frozen contest owner unchanged',record_id=p.record_id,unit_id=p.unit_id,actual_rescue_serials={'peg_ack_at':p11.peg_ack_at,'advance_peg_at':p11.advance_peg_at},base_owner_wording=unit['text'],selected_canonical_wording=p.text,readable_result_completed=vc.active is None,resolved=vc.progress['VC03'].resolved,won=vc.progress['VC03'].won,regression_test='CurrentTests.test_real_rescue_serials_select_exact_current_vc03_result_before_receipt'),indent=2))
