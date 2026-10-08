#!/usr/bin/env python3
"""One first intro case, exact whole-program bindings and per-completed-case receipts."""
from pathlib import Path
import hashlib,json,sys,time,unittest
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H/'tests'));sys.path.insert(0,str(H/'tools'))
from test_intro import Intro
from test_source_reader_after_intro_revision import SourceReaderAfterIntro
from test_confirmation_boundaries import ConfirmationBoundaries
from test_storage_boundaries import StorageBoundaries

def fingerprint():
    paths={p for folder in ('src','templates','tests','tools','inputs','snapshot/resources','toolchain','build/coherent/compiled') for p in (H/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    paths.add(Path(__file__))
    paths.update(p for p in H.iterdir() if p.is_file() and p.suffix=='.py')
    paths.update(H/n for n in ('HOST-SELECTORS.json','HOST-NATIVE-IDS.json','SOURCE-INPUTS.json','selectors.json','COMPOSITION-INPUTS.json'))
    paths.update(H/'build/coherent'/n for n in ('compile-receipt.json','ABI-MAPPINGS.json','selector-list.json'))
    rows={str(p.relative_to(H)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
    return {'sha256':hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest(),'files':rows}

cases=[SourceReaderAfterIntro('test_01_two_page_source_requires_completed_frames_and_restores_partial'),SourceReaderAfterIntro('test_06_cancel_partial_and_reject_corrupt_restore'),Intro('test_01_actual_meeting_partial_close_talk_resume_and_restore'),ConfirmationBoundaries('test_04_final_menu_pointer_numeric_stale_and_real_boundary_guards'),StorageBoundaries('test_03_false_result_explicit_retry_modes_and_inflight_reentry'),StorageBoundaries('test_04_abandoned_return_cannot_ack_restored_snapshot')][:4];identity=fingerprint();assert len(cases)==4
out=H/'evidence/evening-prior-selected-cases.json';proof={'status':'RUNNING','binding':identity,'cases':[],'expected_cases':[c.id() for c in cases],'native_acceptance':False}
def write():
    tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(proof,indent=2)+'\n');tmp.replace(out)
write()
class Result(unittest.TextTestResult):
    def startTest(self,test):self.started=time.monotonic();proof['active_case']=test.id();write();super().startTest(test)
    def addSuccess(self,test):
        super().addSuccess(test);assert fingerprint()==identity
        proof['cases'].append({'case':test.id(),'status':'PASS','seconds':round(time.monotonic()-self.started,3),'binding_sha256':identity['sha256']});proof.pop('active_case',None);write()
    def addFailure(self,test,error):super().addFailure(test,error);proof['cases'].append({'case':test.id(),'status':'FAIL','error':self._exc_info_to_string(error,test)});write()
    def addError(self,test,error):super().addError(test,error);proof['cases'].append({'case':test.id(),'status':'FAIL','error':self._exc_info_to_string(error,test)});write()
r=unittest.TextTestRunner(verbosity=2,resultclass=Result,failfast=True).run(unittest.TestSuite(cases));assert fingerprint()==identity
proof['status']='PASS' if r.wasSuccessful() and len(proof['cases'])==4 else 'FAIL';proof.pop('active_case',None);write();sys.exit(not r.wasSuccessful())
