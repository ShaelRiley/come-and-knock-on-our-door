#!/usr/bin/env python3
"""Review helper collecting the13 already-tested methods; no new gameplay logic."""
from pathlib import Path
import hashlib,json,sys,time,unittest
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H/'tests'),str(H/'tools')]
from test_intro import Intro
from test_intro_negative import IntroNegative
from test_intro_transactions import IntroTransactions
from test_intro_guard import IntroGuard
from test_source_reader_after_intro_revision import SourceReaderAfterIntro

def fingerprint():
    paths={p for folder in ('src','templates','tests','tools','inputs','snapshot/resources','toolchain','build/coherent/compiled') for p in (H/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    paths.update(p for p in H.iterdir() if p.is_file() and p.suffix=='.py')
    paths.update(H/n for n in ('HOST-SELECTORS.json','HOST-NATIVE-IDS.json','SOURCE-INPUTS.json','selectors.json','COMPOSITION-INPUTS.json'))
    paths.update(H/'build/coherent'/n for n in ('compile-receipt.json','ABI-MAPPINGS.json','selector-list.json'))
    rows={str(p.relative_to(H)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
    return {'sha256':hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest(),'files':rows}

intro=sum((list(unittest.defaultTestLoader.loadTestsFromTestCase(c)) for c in (Intro,IntroNegative,IntroTransactions,IntroGuard)),[])
source=list(unittest.defaultTestLoader.loadTestsFromTestCase(SourceReaderAfterIntro))
assert len(intro)==7 and len(source)==6
arg=sys.argv[1] if len(sys.argv)>1 else 'all'
if arg=='--list':
 for c in intro+source:print(c.id())
 sys.exit(0)
assert arg in ('all','intro','source')
cases={'all':intro+source,'intro':intro,'source':source}[arg];identity=fingerprint()
out=H/f'evidence/review-intro-{arg}-cases.json';proof={'status':'RUNNING','binding':identity,'cases':[],'expected_cases':[c.id() for c in cases],'native_acceptance':False}
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
proof['status']='PASS' if r.wasSuccessful() and len(proof['cases'])==len(cases) else 'FAIL';proof.pop('active_case',None);write();sys.exit(not r.wasSuccessful())
