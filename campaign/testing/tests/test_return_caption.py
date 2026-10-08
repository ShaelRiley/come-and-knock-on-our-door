"""Focused real-emitted-bytecode regression, including a red accepted-base oracle.

Kernel/render mocks and typed same-program snapshots are bounded harness evidence,
not native pixels, native saves, audible speech, or acceptance of a new program.
"""
from pathlib import Path
import contextlib,hashlib,json,sys,unittest,gc
sys.dont_write_bytecode=True
import host
from host import act,choice,close,frame,garage,base
from test_practical import enter_control,restore
H=Path(__file__).resolve().parents[1]
BASE=H/'tests/legacy/p05'
VMS=[];OBSERVATIONS=[]
FIRST=['The bread is safely inside. Frankie Maplewood and',
       'Bunny are at the planning board. Read what everyone',
       'was actually invited to.']
RETURN=['JACKIE WALKS TO LIVING ROOM.']

@contextlib.contextmanager
def build(root):
    saved=host.H;host.H=root
    try:yield
    finally:host.H=saved

def track(vm):
    VMS.append(vm);vm.budget=100000000;vm.arrival_events=[]
    def capture(obj,name,args,result):
        if obj.name=='cakood' and name in ['say','navNoticeSet','speechBegin','audioEvent','p02HostEvent']:
            vm.arrival_events.append([name,list(args)])
    vm.after_actual_call=capture
    return vm

def boot(root=H):
    with build(root):vm=track(host.VM())
    h=vm.objects['cakood'];vm.event_queue=[{}]
    try:h.call('play')
    except base.EndOfEvents:pass
    finally:vm.event_queue=None
    h.call('finishOpening')
    assert (h.p['initialized'],h.p['houseEntered'],h.p['location'],h.p['tray'])==(1,0,0,0)
    return h

def first_entry(h,route='bunny',keyboard=False):
    actions={'bunny':[(6,2),(1,5,2),(2,1)],
             'wedge':[(7,5,3),(4,4),(2,1),(7,4,1),(4,5)]}[route]
    for args in actions:act(h,*args)
    if keyboard:keyboard_enter(h)
    else:act(h,0,1)
    assert (h.p['location'],h.p['traySafe'],h.p['houseEntered'],h.p['p01Consumed'])==(1,1,1,1)

def planned(root=H):
    with build(root):t=host.setup()
    h=t[0];track(h.vm)
    # Existing accepted P05 fixture has the agreed plan; normalize its historical
    # one-shot P01 marker, rather than pretending this setup plays the P02 puzzle.
    h.p['p01Consumed']=1
    h.call('p02SyncInventory',1)
    return t

def keyboard_enter(h):
    # Escape is the shipped way to restore default Walk, which has no verb-button
    # control. Stop at the arrival frame so the timed nav notice has not expired.
    h.vm.pump([{'type':4,'message':27},{}])
    assert h.p['uiVerb']==0
    enter_control(h,1,1)
    for _ in range(180):
        if not h.p['motionPhase']:break
        h.vm.pump([{}])
    assert h.p['motionPhase']==0 and h.p['location']==1
    close(h)

def caption(h):
    h.vm.paint=[];h.call('renderCaption');return list(h.vm.paint)

def return_from_porchexit(h,keyboard=False):
    act(h,0,17) # garage -> porch, or court -> porch
    assert h.p['location']==0
    act(h,2,1)
    if keyboard:keyboard_enter(h)
    else:act(h,0,1)
    assert h.p['location']==1

def living_roundtrip(h):
    act(h,0,1);assert h.p['location']==0
    act(h,2,1);act(h,0,1);assert h.p['location']==1

def logical(h):
    vm=h.vm;r=vm.objects['p05State'];v=vm.objects['contestState']
    return {
        'main':{k:x for k,x in h.p.items() if k.startswith('p02') and k not in ['p02Revision','p02PlanOpen'] or k in ['tray','traySafe','houseEntered','p01Consumed','a01Consumed','greetingConsumed']},
        'p02Slots':list(h.arrays['p02Slots']),
        'p05Words':list(r.arrays['p05Words']),'vcWords':list(v.arrays['vcWords']),
        'actors':{k:r.p[k] for k in ['hBunnyRoom','hMiloRoom','hPAOwner','hPARoom','hCartOwner','hCartRoom']},
        'p03Flags':vm.objects['p03State'].p['p03Ready'],
        'p04Flags':vm.objects['p04State'].p['p04Bunting'],
    }

class ReturnCaption(unittest.TestCase):
    def test_actual_first_entry_both_solutions_preserve_exact_full_narration_and_events(self):
        for route in ['bunny','wedge']:
            records=[]
            for root in [BASE,H]:
                h=boot(root);first_entry(h,route,keyboard=(route=='bunny'))
                self.assertEqual(caption(h),FIRST)
                records.append((logical(h),list(h.vm.arrival_events)))
                self.assertEqual(sum(n=='audioEvent' and a==[3] for n,a in h.vm.arrival_events),1)
                self.assertEqual(sum(n=='p02HostEvent' and a[0]==3 for n,a in h.vm.arrival_events),1)
                self.assertTrue(any(n=='speechBegin' and a==[36] for n,a in h.vm.arrival_events))
            self.assertEqual(*records)
            OBSERVATIONS.append({'case':'actual_first_entry_'+route,'caption':FIRST,'source_and_emitted_state_event_parity':True})

    def test_accepted_base_fails_original_native_narrative_regression(self):
        def scenario(root):
            h,d,a,p,q,r=planned(root);act(h,6,2);choice(h,209,1)
            self.assertEqual((r.p['hBunnyRoom'],h.p['location']),(5,5))
            return_from_porchexit(h)
            self.assertEqual(r.p['hBunnyRoom'],5)
            self.assertEqual(h.call('campaignReachable',2),0)
            return caption(h),logical(h)
        before,oldstate=scenario(BASE);after,newstate=scenario(H)
        self.assertEqual(before,FIRST)
        with self.assertRaises(AssertionError):self.assertEqual(before,RETURN)
        self.assertEqual(after,RETURN);self.assertEqual(oldstate,newstate)
        OBSERVATIONS.append({'case':'native_absent_bunny_red_green','accepted_base_expected_failure':before,'corrected':after,'puzzle_actor_state_equal':True})

    def test_repeated_entries_with_bunny_home_do_not_repeat_p01_or_p02_grants(self):
        h=boot();first_entry(h)
        before=logical(h);events=len(h.vm.arrival_events)
        for _ in range(3):
            living_roundtrip(h);self.assertEqual(caption(h),RETURN)
            self.assertEqual(logical(h),before)
        calls=h.vm.arrival_events[events:]
        self.assertFalse(any(n in ['say','speechBegin'] and a==[36] for n,a in calls))
        self.assertFalse(any(n in ['audioEvent','p02HostEvent'] and a[0]==3 for n,a in calls))

    def test_repeated_entries_after_valid_invitation_preserve_absence_and_practical_state(self):
        h,d,a,p,q,r=planned();act(h,6,2);choice(h,209,1)
        for args in [(7,65,66),(7,64)]:act(h,*args)
        choice(h,212,1);act(h,8,68);choice(h,213,1);act(h,6,65);choice(h,214,1)
        self.assertEqual(r.call('p05Flags'),1)
        before=logical(h)
        return_from_porchexit(h,keyboard=True)
        for _ in range(3):
            self.assertEqual(caption(h),RETURN)
            self.assertEqual(logical(h),before)
            h.call('uiBuildFocus')
            self.assertFalse(any(h.arrays['uiActions'][i]==1 and h.arrays['uiPayloads'][i]==2 for i in range(h.p['uiControlCount'])))
            self.assertEqual(h.call('dialogueCanSpeak',2),0)
            living_roundtrip(h)

    def test_valid_bunny_home_return_retains_controls_and_next_arrival_is_generic(self):
        h,d,a,p,q,r=planned();act(h,6,2);choice(h,209,1)
        act(h,6,2);choice(h,209,2)
        self.assertEqual((r.p['hBunnyRoom'],h.p['location'],r.arrays['p05Words'][69]),(1,1,0))
        h.call('uiBuildFocus')
        self.assertTrue(any(h.arrays['uiActions'][i]==1 and h.arrays['uiPayloads'][i]==2 for i in range(h.p['uiControlCount'])))
        before=logical(h);living_roundtrip(h)
        self.assertEqual(caption(h),RETURN);self.assertEqual(logical(h),before)
        self.assertEqual(h.call('dialogueCanSpeak',2),1)

    def test_same_program_save_ready_snapshot_restore_before_and_after_return(self):
        for away in [False,True]:
            h,d,a,p,q,r=planned()
            if away:act(h,6,2);choice(h,209,1);return_from_porchexit(h)
            before=logical(h)
            for phase in ['before','after']:
                if phase=='after':living_roundtrip(h)
                self.assertEqual(r.call('hSaveReady'),1)
                saved=h.vm.snapshot();restore(h,saved,[{},{}])
                self.assertEqual((r.p['hRestoreValid'],h.p['uiFailure']),(1,0))
                self.assertEqual(logical(h),before)
                living_roundtrip(h);self.assertEqual(caption(h),RETURN)
                self.assertEqual(logical(h),before)
        OBSERVATIONS.append({'case':'ordinary_same_program_restore_path','states':['Bunny home before/after return','Bunny garage before/after return'],'native_save':False,'boundary':'typed harness serialization through real emitted replay/restore validation; native recheck required'})

    def test_closed_door_and_uncollected_tray_keep_original_blockers(self):
        for root in [BASE,H]:
            h=boot(root);act(h,0,1);self.assertEqual((h.p['location'],h.p['houseEntered'],h.p['currentCaption']),(0,0,33))
            act(h,7,5,3);act(h,2,1);act(h,0,1)
            self.assertEqual((h.p['location'],h.p['houseEntered'],h.p['currentCaption']),(0,0,35))
            self.assertEqual(h.p['navNotice'],0)

    def test_source_adapter_scope_guards_and_nonmutation(self):
        sys.path.insert(0,str(H));from adapt_return_caption import transform,BASE_MAIN_SHA
        from source_tools import methods
        before=(H/'fixtures/main.before.sc').read_bytes();after=(H/'snapshot/base/main.caption-fixed.sc.txt').read_text()
        self.assertEqual(hashlib.sha256(before).hexdigest(),BASE_MAIN_SHA)
        self.assertEqual(before,(BASE/'src/main.sc').read_bytes())
        self.assertEqual(transform(before.decode()),after)
        with self.assertRaises(ValueError):transform(after)
        with self.assertRaises(ValueError):transform(before.decode().replace('(self say: 36)','(self say: 35)'))
        a,b=methods(before.decode()),methods(after)
        self.assertEqual(methods((H/'src/main.sc').read_text())['walk'],b['walk'])
        self.assertEqual([n for n in a if a[n]!=b[n]],['walk'])
        for name in ['renderCaption','speechStart','speechBegin','p02Delegate','p02Act','navNoticeSet','navNoticeRender']:
            self.assertEqual(a[name],b[name])

if __name__=='__main__':
    (H/'evidence/return-caption-tests.json').write_text('{"status":"RUNNING","native_acceptance":false}\n')
    metrics=[]
    class Result(unittest.TextTestResult):
        def stopTest(self,test):
            metrics.append({'test':test.id(),'instructions':sum(v.steps for v in VMS),'frames':sum(v.frames for v in VMS)})
            VMS.clear();gc.collect();super().stopTest(test)
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ReturnCaption)
    ids=[t.id().replace("__main__.","test_return_caption.") for t in suite]
    expected=json.loads((H/'tests/EXPECTED-RETURN-TESTS.json').read_text())
    if len(ids)!=len(set(ids)) or sorted(ids)!=expected:raise RuntimeError('Focused test identity mismatch')
    result=unittest.TextTestRunner(verbosity=2,resultclass=Result).run(suite)
    report={'status':'PASS' if result.wasSuccessful() and result.testsRun==len(expected) and not result.skipped else 'FAIL','tests':result.testsRun,'test_ids':ids,'skipped':result.skipped,'failures':[(str(t),s) for t,s in result.failures],'errors':[(str(t),s) for t,s in result.errors],'metrics':metrics,'observations':OBSERVATIONS,'native_acceptance':False}
    (H/'evidence/return-caption-tests.json').write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(report['status']!='PASS')
