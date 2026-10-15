#!/usr/bin/env python3
"""Emitted P11 group geometry/anchor checks; explicit fixtures, never native acceptance."""
import argparse,hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
SOURCE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(SOURCE/'tests'),str(SOURCE/'tools')]
from presentation_vm import PresentationVM
from source_tools import methods
from inspect_opening_view import decode_view
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
class AnchorFixture(PresentationVM):
    """Scene coordinates only; no campaign progression or save fixture."""
    def __init__(self, build):
        super().__init__(build)
        self.guard = True
        self.h.p.update(location=3, onApron=0, motionPhase=0, motionPose=0,
                        p06=0, paused=0, opening=0, menuOpen=0, uiFailure=0)

    def call(self, obj, name, args=()):
        if obj.module.number == 993 and name == 'h11PayGuard':
            # Only admission to the unchanged anchor comparison is modeled.
            # Separate false cases below exercise its rejection behavior.
            return int(self.guard)
        return super().call(obj, name, args)

def snapshot(v, ignore_pay=False):
    return {'properties': {n: dict(v.instance(n).p) for n in (993, 994, 995, 996)},
            'locals': {n: {k: list(a) for k, a in v.arrays(n).items()
                           if not (ignore_pay and n == 993 and k == 'h11Pay')}
                       for n in (993, 994, 995, 996)},
            'main': dict(v.h.p)}

def projected_pixels(packet):
    view, loop, cel, left, top, _, *scale = packet
    item = decode_view((SOURCE / 'assets/resources' / f'{view}.view.bin').read_bytes())[loop][cel]
    sx, sy = scale if len(scale) == 2 else (128, 128)
    if not sx:
        sx = sy = 128
    w = item['width']
    # Integer projection is a geometry model, not stock ScummVM's rasterizer.
    return {(left + (index % w) * sx // 128,
             top + (index // w) * sy // 128)
            for index, value in enumerate(item['pixels'])
            if value != item['clear_key']}

def geometry(v, anchor, facing):
    v.h.p.update(motionX=anchor[0] * 64, motionY=anchor[1] * 64,
                 motionLoop=facing, motionPose=0, motionPhase=0)
    before = snapshot(v)
    v.h.draws.clear()
    v.call(v.h, 'drawJack')
    v.call(v.h, 'p04Felix')
    assert snapshot(v) == before, 'Idle drawing changed owner/domain/Main state'
    jack = next(p for p in v.h.draws if p[0] == 214)
    felix = next(p for p in v.h.draws if p[0] == 225)
    jp, fp = projected_pixels(jack), projected_pixels(felix)
    return {'facing': facing, 'anchor': anchor,
            'projected_opaque_overlap_pixels': len(jp & fp),
            'jack_opaque_bottom': max(y for x, y in jp),
            'felix_opaque_bottom': max(y for x, y in fp),
            'jack_draw': jack, 'felix_draw': felix}

def transient_anchor_cases(v, anchor):
    owner = v.instance(993)
    pay = v.arrays(993)['h11Pay']
    cases = []

    def prepare():
        pay[:] = [0] * len(pay)
        pay[0] = 2
        pay[8], pay[9] = anchor[0] * 64, anchor[1] * 64
        v.guard = True

    for obj in range(415, 419):
        prepare()
        before, stable = list(pay), snapshot(v, ignore_pay=True)
        assert v.call(owner, 'h11PayMove', (*anchor, 5, obj)) == 1
        before[24] = 1
        assert list(pay) == before and snapshot(v, ignore_pay=True) == stable
        cases.append(f'same valid waiting anchor preserved for group object{obj}')
    negatives = [(*anchor, 7, 415), (*anchor, 5, 414), (*anchor, 5, 419),
                 (anchor[0] + 1, anchor[1], 5, 415),
                 (anchor[0], anchor[1] + 1, 5, 415), (150, 120, 5, 415)]
    for values in negatives:
        prepare()
        stable = snapshot(v, ignore_pay=True)
        v.call(owner, 'h11PayMove', values)
        assert not any(pay) and snapshot(v, ignore_pay=True) == stable
        cases.append('mismatched point/verb/object retires transient proof: ' + str(values))
    prepare()
    v.guard = False
    stable = snapshot(v, ignore_pay=True)
    v.call(owner, 'h11PayMove', (*anchor, 5, 415))
    assert not any(pay) and snapshot(v, ignore_pay=True) == stable
    cases.append('failed unchanged admission retires proof, never waived for repaired point')
    prepare()
    pay[0] = 0
    before = list(pay)
    assert v.call(owner, 'h11PayMove', (*anchor, 5, 415)) == 1 and list(pay) == before
    cases.append('inactive presentation remains inactive')
    return cases

def run(build=None):
 build=Path(build) if build else SOURCE/'build/coherent'
 fixture=json.loads((SOURCE/'tests/fixtures/P11-R8-REPAIR-REFERENCE.json').read_text())
 current=methods((SOURCE/'src/main.sc').read_text())
 assert digest(SOURCE/'src/main.sc')==fixture['candidate_main_sha256']
 core=json.loads((SOURCE/'CORE-PRESERVATION.json').read_text())
 for name,pin in fixture['candidate_methods_sha256'].items():
  assert hashlib.sha256(current[name].encode()).hexdigest()==pin
  row=next(x for x in core['reviewed_modified_methods'] if x['file']=='main.sc' and x['method']==name)
  assert row['candidate_sha256']==pin and row['baseline_sha256']==fixture['baseline_methods_sha256'][name]
 for number,pin in fixture['original_art_sha256'].items():assert digest(SOURCE/'assets/resources'/f'{number}.view.bin')==pin
 receipt=json.loads((build/'compile-receipt.json').read_text())
 main=next(x for x in receipt['modules'] if x['module']==0)
 assert main['source_sha256']==digest(SOURCE/'src/main.sc')
 assert main['script_sha256']==digest(build/'compiled/0.scr.bin')
 assert main['heap_sha256']==digest(build/'compiled/0.scr.bin.hep')
 assert receipt['phase']=='B' and receipt['native_acceptance'] is False
 v=AnchorFixture(build)
 cases=['reviewed three source methods and original art bound to explicit frozen reference; other preservation is checked by source gate',
        'actual emitted Main script/heap and source identity match the fresh candidate receipt']
 expected=tuple(v.call(v.h,'p04Approach'+a,(54,)) for a in ('X','Y'))
 assert expected==tuple(fixture['expected_existing_felix_anchor'])
 for obj in range(415,419):
  before=snapshot(v)
  assert tuple(v.call(v.h,'approach'+a,(obj,)) for a in ('X','Y'))==expected
  assert snapshot(v)==before
  cases.append('actual emitted read-only group approach '+str(obj)+' reuses established Felix point')
 for obj,point in fixture['repaired_rack_approaches'].items():
  before=snapshot(v)
  assert tuple(v.call(v.h,'approach'+a,(int(obj),)) for a in ('X','Y'))==tuple(point)
  assert snapshot(v)==before
  cases.append('actual emitted read-only rack approach '+obj+' grounds feet without changing X')
 for obj,point in fixture['baseline_neighbor_approaches'].items():
  before=snapshot(v)
  assert tuple(v.call(v.h,'approach'+a,(int(obj),)) for a in ('X','Y'))==tuple(point)
  assert snapshot(v)==before
  cases.append('unrelated neighboring approach '+obj+' retains frozen emitted result')
 geometry_results=[]
 for facing in (0,1):
  old=geometry(v,tuple(fixture['baseline_defective_anchor']),facing);new=geometry(v,expected,facing)
  assert old['jack_opaque_bottom']<old['felix_opaque_bottom']
  assert new['jack_opaque_bottom']>=new['felix_opaque_bottom']
  assert new['projected_opaque_overlap_pixels']<old['projected_opaque_overlap_pixels']/4
  geometry_results.append({'baseline_anchor':old,'candidate_anchor':new})
  cases.append('unchanged original-art emitted idle drawing facing'+str(facing)+' removes elevated floor depth and reduces actor overlap')
 # Late Courtyard uses the unchanged fixed scale127 whenever p05 exists.
 # p05=1 is a truthy-only motionScale fixture here; no p05 method is called.
 v.h.p.update(location=4,p05=1)
 for facing in (0,1):
  bounds=[]
  for anchor in (fixture['baseline_defective_rack_anchor'],fixture['repaired_rack_approaches']['410']):
   v.h.p.update(motionX=anchor[0]*64,motionY=anchor[1]*64,motionLoop=facing)
   before=snapshot(v);v.h.draws.clear();v.call(v.h,'drawJack');assert snapshot(v)==before
   packet=next(p for p in v.h.draws if p[0]==214);pixels=projected_pixels(packet)
   bounds.append({'anchor':anchor,'draw':packet,'opaque_bounds':[min(x for x,y in pixels),min(y for x,y in pixels),max(x for x,y in pixels)+1,max(y for x,y in pixels)+1],
                  'header_overlap':sum(y<43 for x,y in pixels),'serve_caption_overlap':sum(168<=x<320 and 44<=y<52 for x,y in pixels),'footer_overlap':sum(y>=144 for x,y in pixels)})
  assert bounds[0]['header_overlap']>0 and bounds[0]['serve_caption_overlap']>0
  assert bounds[1]['header_overlap']==bounds[1]['serve_caption_overlap']==bounds[1]['footer_overlap']==0
  assert bounds[1]['opaque_bounds'][3]>=138 and tuple(bounds[1]['draw'][6:])==(127,127)
  geometry_results.append({'rack_baseline':bounds[0],'rack_candidate':bounds[1]})
  cases.append('unchanged Courtyard original-art facing'+str(facing)+' clears header/caption and remains grounded above footer')
 # Existing owner-family branches remain authoritative over their own objects.
 for number,array,obj in ((995,'h13Lease',432),(996,'h14Owner',25)):
  state=v.arrays(number)[array];old=state[0];state[0]=1;before=snapshot(v)
  assert tuple(v.call(v.h,'approach'+a,(obj,)) for a in ('X','Y'))==(180,128)
  for rack in (410,411):assert tuple(v.call(v.h,'approach'+a,(rack,)) for a in ('X','Y'))==(200,138)
  assert snapshot(v)==before;state[0]=old
  cases.append('unchanged owner family'+str(number)+' approach precedence and rack exclusion retained')
 v.h.p.update(location=3,p05=0)
 cases+=transient_anchor_cases(v,expected)
 return {'status':'PASS_EMITTED_NOT_NATIVE','case_count':len(cases),'cases':cases,'geometry':geometry_results,
         'compile_receipt_sha256':digest(build/'compile-receipt.json'),'native_acceptance':False,'observed':None,
         'limits':['Location/motion and PayGuard admission are explicit unit fixtures, never earned campaign state.',
                  'Actual compiled Main approach and unchanged drawing/PayMove execute; opaque geometry models integer projection, not stock native pixels.',
                  'Full Fold→Close→ordinary control→Stage and natural modeled EOF are checked separately.',
                  'No GUI,input,native saves,acoustic or full-campaign acceptance.']}

if __name__=='__main__':
 q=argparse.ArgumentParser();q.add_argument('--build',type=Path);q.add_argument('--output',type=Path);a=q.parse_args()
 result=run(a.build)
 if a.output:
  assert not a.output.exists(),'Refuse to overwrite prior evidence'
  a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result))
