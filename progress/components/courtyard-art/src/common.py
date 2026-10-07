"""Shared pure geometry/IO utilities; no generation or verification on import."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent.parent

def require(ok,message):
    if not ok: raise ValueError(message)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write_json(path,obj):Path(path).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
class Guard:
    def __init__(self,name):
        self.name=name;self.path=ROOT/'evidence'/f'{name}.json';self.write('RUNNING')
        if name in ['build','preview','encode_indexed']:
            write_json(ROOT/'evidence/validation.json',{'status':'STALE','reason':name+' started; rerun validation'})
        sys.excepthook=self.fail
        if sys.flags.optimize:
            self.write('FAIL',error='Optimized Python is not an accepted verification mode');raise SystemExit(2)
    def write(self,status,**kw):write_json(self.path,{'status':status,'tool':self.name,**kw})
    def fail(self,typ,error,tb):self.write('FAIL',error=str(error));sys.__excepthook__(typ,error,tb)
    def done(self,**kw):self.write('PASS',**kw)
