from pathlib import Path
import subprocess,sys,json
H=Path(__file__).resolve().parents[1]
class Owner:
 def __init__(self,kind='emitted',date='Explicit selected fixture',stage='readback',urls=()):
  self.process=subprocess.Popen([sys.executable,'-B',str(H/'tests/domain_owner.py')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
  self.request('prepare',kind=kind,date=date,stage=stage,urls=list(urls))
 def request(self,op,**kw):
  self.process.stdin.write(json.dumps(dict(op=op,**kw))+'\n');self.process.stdin.flush();line=self.process.stdout.readline()
  if not line:raise RuntimeError('Owner process stopped: '+self.process.stderr.read())
  reply=json.loads(line)
  if 'error' in reply:raise RuntimeError(reply['trace'])
  return reply['result']
 @property
 def p(self):return self.request('properties')
 def call(self,name,*args):return self.request('call',name=name,args=list(args))
 def close(self):
  if self.process.poll() is None:self.request('stop');self.process.wait(timeout=10)
  for stream in (self.process.stdin,self.process.stdout,self.process.stderr):stream.close()
 def __enter__(self):return self
 def __exit__(self,*args):self.close()
