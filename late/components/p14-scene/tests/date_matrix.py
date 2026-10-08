"""Bounded emitted date-caption matrix; synthetic inputs never select game dates."""
from pathlib import Path
import sys,json
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H),str(H/'tests'),str(H/'tools')]
from host import setup
from test_runtime import bind
index=int(sys.argv[1]);assert 0<=index<8
h,d,a,*_=setup();alphabet=''.join(chr(c) for c in range(32,127) if c!=124);template=next(r['text'] for r in json.loads((H/'inputs/canonical-bindings.json').read_text())['records'] if r['id']=='P14.READ.001');cases=[]
for n in range(index*10+1,index*10+11):
 text=''.join(alphabet[(i*7+n)%len(alphabet)] for i in range(n));bind(h.vm,d,text);assert d.call('sdOpen',1800,0,0,0,a)==1;parts=[]
 for page in range(d.p['sdCount']):
  if page:assert d.call('sdTurn',1,a)==1
  assert d.call('sdDraw',0)==1;parts.append(str(d.arrays['sdTextBuffer']).replace('\n',''));assert d.p['sdVoice']==0 and d.p['sdAudioModule']==0
 assert ''.join(parts)==template.format(repair_date=text);cases.append(n)
report=dict(status='PASS',bank=index,selected_synthetic_lengths=cases,emitted_instructions=h.vm.steps,maximum_date_chars=80,pipe_rejected_separately=True,exact_every_character=True,native_acceptance=False)
(H/f'evidence/date-matrix-{index}.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
