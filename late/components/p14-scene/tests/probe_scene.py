from pathlib import Path
import sys,json
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H),str(H/'tests'),str(H/'tools')]
from host import setup,frame,base
h,d,a,*_=setup();vm=h.vm
m=json.loads((H/'generated/manifest.json').read_text())
for r in m['document_routes']:
 assert d.call('sdOpen',r['document_id'],0,0,0,a)==1,(r['record_id'],d.p['sdFailure'])
 for pn,pi in enumerate(r['page_indices']):
  if pn:assert d.call('sdTurn',1,a)==1
  assert d.call('sdDraw',0)==1,(r['record_id'],pn,d.p['sdFailure'])
  assert str(d.arrays['sdTextBuffer'])==m['pages'][pi]['text']
print('PASS',len(m['document_routes']),'routes',len(m['pages']),'pages',vm.steps,'instructions')
def export(n,*args):
 bank=vm.modules[999];return vm.execute(d,bank,'export'+str(n),bank.layout['exports'][n],args)
for date in ['A','MiXeD'+('a'*75),' '*80,'A{B}~c@D#']:
 assert export(2,996,1,0,1,0,1,0,1,len(date))==1
 for i,c in enumerate(date):assert export(3,i,ord(c))==1
 assert export(4)==1
 raw=next(r['text'] for r in m['canonical_records'] if r['id']=='P14.READ.001').format(repair_date=date)
 assert d.call('sdOpen',1800,0,0,0,a)==1
 out=[]
 for pn in range(d.p['sdCount']):
  if pn:assert d.call('sdTurn',1,a)==1
  assert d.call('sdDraw',0)==1
  out.append(str(d.arrays['sdTextBuffer']).replace('\n',''))
  assert d.p['sdVoice']==0 and d.p['sdAudioModule']==0
 assert ''.join(out)==raw,repr((''.join(out),raw))
print('PASS dynamic date shapes',vm.steps)
