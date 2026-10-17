#!/usr/bin/env python3
"""Emitted FIFO/modal date transaction tests; scene admission modeled, real guards checked separately."""
import argparse
import json
from pathlib import Path
import sys
import traceback
import check_date_modal as date
from check_date_modal import QueueFixture, NormalEngineQuit, key, FIELDS

# Extend the older modal fixture's typed kernel model only for an empty FIFO.
# Its existing11 publication assertions stay untouched; this adds no admission.
_original_kernel = date.DateFixture.kernel
def empty_fifo_kernel(self, number, args):
    if self.knames.get(number) == 'GetEvent':
        assert len(args) == 2 and args[1] is self.h and args[0] & 0xffff in (65535,32767)
        self.h.p.update(type=0,message=0,modifiers=0,x=319,y=199)
        return 0
    return _original_kernel(self, number, args)
date.DateFixture.kernel = empty_fifo_kernel

class Fixture(QueueFixture):
    def input_event(self, event):
        self.h.p.update({f:event[f] for f in FIELDS})
        return self.call(self.instance(996),'h14Input')

def run(build):
    cases=[]
    old=date.run(build)
    assert old['status']=='PASS_EMITTED_NOT_NATIVE' and old['case_count']==11
    cases.append({'name':'unchanged11modal-publication-regressions','result':old})
    v=Fixture(build)
    v.pending_events.append(key(32768,8))
    for c in 'BCDEFGHIJKLMNOPQRST':v.pending_events.extend([key(ord(c)),key(32768,8)])
    assert v.input(ord('A'))==1 and v.text()=='ABCDEFGHIJKLMNOP'
    assert len(v.consumed)==31 and len(v.pending_events)==8 and v.base_calls==2
    assert v.pending_events[0]['message']==ord('Q') and not v.date()
    assert v.arrays(996)['h14Edit'][3]==0 and v.arrays(996)['h14Batch'][0]==0
    assert list(v.arrays(996)['h14BatchEdit'])==[0]*5 and list(v.arrays(996)['h14BatchChars'])==[0]*80
    assert v.fields()=={f:v.consumed[-1][f] for f in FIELDS}
    v.render(); assert v.arrays(996)['h14Edit'][3]==1
    before=v.base_calls
    assert v.ordinary_next()==1 and v.text()=='ABCDEFGHIJKLMNOPQRST' and not v.pending_events
    assert v.base_calls-before==2 and v.arrays(996)['h14Edit'][3]==0 and not v.date()
    cases.append({'name':'32events16chars/two-original-strict-admissions/one-batch-before-paint','extra_events':31})
    v=Fixture(build)
    e=dict(type=4,message=ord('A'),modifiers=7,x=219,y=103)
    assert v.input_event(e)==1 and v.fields()==e and v.base_calls==2
    assert len(v.polls)==1 and v.polls[0]['peek']
    cases.append({'name':'single physical key+emptyPeek restores all5fields'})
    barriers=[key(13),key(27),key(9),key(15360),key(15616),key(31),key(127),
        dict(type=1,message=7,modifiers=3,x=99,y=113),
        dict(type=2,message=8,modifiers=1,x=78,y=124),
        dict(type=64,message=2,modifiers=4,x=67,y=134)]
    for barrier in barriers:
        v=Fixture(build);v.pending_events.extend([barrier,key(ord('B'))])
        v.h.p.update(modifiers=5,x=44,y=123)
        assert v.input(ord('A'))==1 and v.text()=='A' and not v.consumed
        assert list(v.pending_events)==[barrier,key(ord('B'))]
        assert v.fields()==dict(type=4,message=ord('A'),modifiers=5,x=44,y=123)
        assert v.base_calls==2 and not v.date()
    cases.append({'name':'10 FIFO barriers stay head and all5fields restored','barrier_types':[b['type'] for b in barriers]})
    v=Fixture(build)
    enter=key(13);v.pending_events.extend([key(ord('B')),key(32768,8),enter,key(ord('C'))])
    assert v.input(ord('A'))==1 and v.text()=='AB' and not v.date()
    assert v.pending_events[0]==enter and v.arrays(996)['h14Edit'][3]==0
    assert v.fields()=={f:v.consumed[-1][f] for f in FIELDS}
    v.render(); assert date.overlay_last(v) and v.arrays(996)['h14Edit'][3]==1
    assert v.ordinary_next()==1 and v.date()=='AB' and v.pending_events[0]['message']==ord('C')
    assert v.arrays(996)['h14Edit'][0]==0
    cases.append({'name':'Enter remains FIFO barrier until actual strict Main paint then literal commit'})
    v=Fixture(build,text='seed');assert v.input(13)==1 and not v.date() and v.arrays(996)['h14Edit'][0]==1
    cases.append({'name':'Enter cannot commit before acknowledged paint'})
    v=Fixture(build);v.pending_events.extend([key(ord('|')),key(ord('B'))])
    assert v.input(ord('A'))==1 and v.text()=='A' and v.arrays(996)['h14Edit'][2]==1
    assert v.pending_events[0]['message']==ord('B') and v.arrays(996)['h14Edit'][3]==0
    v.render();assert 'Unsupported character or date too long.' in v.paint
    assert v.ordinary_next()==1 and v.text()=='AB' and v.arrays(996)['h14Edit'][2]==0
    cases.append({'name':'unsupported pipe stops batch/visible warning then ordinary editing recovers'})
    v=Fixture(build,text='A'*79);v.pending_events.extend([key(ord('C')),key(ord('D'))])
    assert v.input(ord('B'))==1 and len(v.text())==80 and v.arrays(996)['h14Edit'][2]==1
    assert v.pending_events[0]['message']==ord('D')
    v=Fixture(build,text='A'*80);assert v.input(8)==1 and v.text()=='A'*79
    assert v.arrays(996)['h14Edit'][3]==0;v.render();v.input(13);assert v.date()=='A'*79
    cases.append({'name':'80char limit and Backspace/repaint/exact Enter unchanged'})
    v=Fixture(build,text='seed');v.pending_events.append(key(27));v.input(ord('!'))
    assert v.pending_events[0]['message']==27;v.ordinary_next()
    assert not v.date() and v.arrays(996)['h14Edit'][0]==0 and v.arrays(996)['h14Batch'][0]==0
    cases.append({'name':'ordinary Escape after batch cancels without committed date'})
    for operation,args in [('h14Save',()),('h14Load',(0,)),('h14Load',(1,)),('h14Load',(2,))]:
        v=Fixture(build,text='seed');v.input(ord('!'))
        assert v.arrays(996)['h14Batch'][0]==0
        v.call(v.instance(996),operation,args)
        assert v.arrays(996)['h14Edit'][0]==0 and not v.date()
        assert v.arrays(996)['h14Batch'][0]==0
        assert list(v.arrays(996)['h14BatchEdit'])==[0]*5 and list(v.arrays(996)['h14BatchChars'])==[0]*80
    cases.append({'name':'actual Save and all Load phases clear transient admission/backups/editor'})
    v=Fixture(build)
    v.pending_events.append(dict(type=2048,message=0,modifiers=0,x=0,y=0))
    try:v.input(ord('A'));raise AssertionError('Expected stock-modeled Quit abort')
    except NormalEngineQuit:assert not v.consumed and len(v.pending_events)==1
    cases.append({'name':'all-events Peek retains modeled native Quit abort; no quit suppression'})
    return {'status':'PASS_EMITTED_NOT_NATIVE','case_groups':len(cases),'cases':cases,'native_acceptance':False,
      'scope':'Actual emitted new date input/drain, original literal bank/Return/Escape, actual Main strict paint/publication. Complemented by separate real-guard suite.',
      'modeled':'This FIFO/modal suite models h14Base admission and prior scene/renderer. It provides no native speed/audio/progression evidence.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--build');p.add_argument('--output');a=p.parse_args()
    try:r=run(a.build)
    except BaseException as error:
        r={'status':'FAILED_EMITTED_TEST','error':str(error),'traceback':traceback.format_exc(),'native_acceptance':False}
    if a.output:
        out=Path(a.output)
        with out.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
    print(json.dumps(r))
    raise SystemExit(0 if r['status']=='PASS_EMITTED_NOT_NATIVE' else 2)
