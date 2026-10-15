#!/usr/bin/env python3
"""Emitted Fold→Close→ordinary Look→Stage regression; explicit ancestors/device fixtures, never native acceptance."""
from pathlib import Path
import argparse,hashlib,json,time,sys
sys.dont_write_bytecode=True
from p11_fold_fixture import prepare_closed, SOURCE


def run(build, expect_fixed, progress=None):
    began=time.monotonic();v,fold=prepare_closed(build);p=v.instance(993)
    closed=v.snapshot()  # Portable emitted unit-state branch, never a SCI save.
    cases=[]
    def log(row):
        if progress is None:return  # Optional internal progress is off by default.
        with progress.open('a') as stream:stream.write(json.dumps({'elapsed':time.monotonic()-began,**row})+'\n')
    log({'event':'START','expect_fixed':expect_fixed})
    def restore():
        v.restore(closed);v.steps=0;v.event_calls=[];v.pay_events=[]
        v.track_route=True;v.owner_good=True
    def entry(obj=415):
        v.call(v.h,'uiBuildFocus')
        actions=v.arrays(0)['uiActions'];payloads=v.arrays(0)['uiPayloads']
        index=next(i for i in range(v.h.p['uiControlCount']) if actions[i]==1 and payloads[i]==obj)
        v.call(v.h,'uiActivate',(index,))
    def record(label, expected):
        pay=v.arrays(993)['h11Pay'];assert pay[0]==expected,(label,pay[0],v.event_calls)
        cases.append({'case':label,'payoff_mode':pay[0],'domain_valid':v.call(p,'p11Validate'),
                      'fold_complete':v.call(p,'p11Complete',(7,))})
        log(cases[-1])
    # Actual uiBuildFocus→uiActivate(action1)→uiChooseObject→uiHostAct→
    # motionRequest→same-anchor arrival→h11Dispatch→h11Menu.
    for obj in (415,416,417,418):
        restore();entry(obj)
        record(f'ordinary same-anchor Look group{obj}',2 if expect_fixed else 0)
        assert v.h.p['uiPanel']==2 and v.h.p['uiChoiceContext']==250
        assert v.h.p['uiChoiceCount']==14
    if not expect_fixed:
        return {'status':'BASELINE_DEFECT_REPRODUCED_EMITTED_NOT_NATIVE','fold':fold,'cases':cases,
                'native_acceptance':False,'seconds':time.monotonic()-began}
    # Strict failures do not receive a continuation; existing cancellation runs.
    for label,mutate,args in (
        ('different verb',lambda:None,(6,415,0)),
        ('non-group object',lambda:None,(5,54,0)),
        ('second noun target',lambda:None,(5,415,42)),
        ('changed X anchor',lambda:v.h.p.update(motionX=v.h.p['motionX']+64),(5,415,0)),
        ('changed Y anchor',lambda:v.h.p.update(motionY=v.h.p['motionY']+64),(5,415,0)),
        ('changed fold serial',lambda:p.p.update(p11FoldLo=p.p['p11FoldLo']+1),(5,415,0)),
    ):
        restore();mutate();v.call(v.h,'uiHostAct',args);record(label,0)
    for label,method,args in [('Save barrier','h11Save',()),('Load barrier','h11Load',(0,))]:
        restore();v.call(p,method,args);record(label,0)
    # Ordinary menu paging must retain the proof, then actual scored-domain
    # Stage action must enter its finite mode3 without granting a forged laugh.
    restore();entry()
    for i in range(5):v.call(v.h,'uiTurnPage',(1,))
    assert v.h.p['uiPage']==5 and v.h.p['uiChoiceCount']==14
    actions=v.arrays(0)['uiActions']
    index=next(i for i in range(v.h.p['uiControlCount']) if actions[i]==13)
    v.call(v.h,'uiActivate',(index,))
    pay=v.arrays(993)['h11Pay']
    assert pay[0]==3 and pay[1]==7 and v.call(p,'p11Ready')==1
    assert v.call(p,'p11Present',(10,))==0
    cases.append({'case':'ordinary 6/14 Stage enters finite mode3 after all guards',
                  'payoff_mode':pay[0],'domain_stage_ready':1,'laugh_claimed_before_paint':False})
    v.call(v.h,'render');v.call(v.h,'dialoguePresented')
    d=v.h.p['dialogue']
    assert d.p['sdAudioToken']==v.a.p['token'] and v.a.p['lane']==1
    v.audio_position=-1;v.call(v.a,'poll',(v.now,v.a.p['token']))
    for i in range(12):v.now+=6;v.call(v.h,'render')
    frames=sorted({draw[2] for draw in v.h.draws if draw[0]==240})
    assert frames==list(range(7)),frames
    assert v.call(p,'p11Complete',(8,))==1 and v.call(p,'p11Present',(10,))==1
    assert pay[0]==0 and v.call(p,'p11Validate')==1
    claims=sum(e['method']=='p11ClaimLaugh' for e in v.event_calls)
    assert claims==1,claims
    cases.append({'case':'actual Stage paint0..6 natural voice EOF actual domain laugh claim once',
                  'painted_stage_cels':frames,'actual_stage_complete':1,'actual_laugh_claim_count':claims,
                  'native_audio_accepted':False})
    return {'status':'PASS_EMITTED_NOT_NATIVE','fold':fold,'cases':cases,
            'case_count':len(cases),'seconds':time.monotonic()-began,'native_acceptance':False,
            'scope':'Real P11 ledger operations/validator, fullFoldreader/render/audioEOF/Close, actualfocuscontrolactivation→motion/menu/choice→Stagepaint/domainclaim. Earlier campaign admissions and device kernels explicitly modeled in trace probes. Portable checkpoint is only an emitted unit-state branch, not a native save.'}

if __name__=='__main__':
    q=argparse.ArgumentParser();q.add_argument('--build',type=Path);q.add_argument('--expect-fixed',action='store_true');q.add_argument('--output',type=Path,required=True);a=q.parse_args()
    if a.output.exists():q.error('Refuse to overwrite previous test evidence')
    result=run(a.build,a.expect_fixed)
    result['build_receipt_sha256']=hashlib.sha256(((a.build or SOURCE/'build/coherent')/'compile-receipt.json').read_bytes()).hexdigest()
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','seconds','build_receipt_sha256')}))
