"""Independent legal owner joins and P12/source continuation probes.

Uses actual accepted owners. Only the supplied test-only variant projection is
imported as the reviewed subject; no supplied P12 Harness or gameplay helpers.
"""
from pathlib import Path
from dataclasses import replace
import copy,itertools,json,sys,traceback
R=Path(__file__).resolve().parents[1];P=R/'reference';C=P/'component';D=R
sys.path[:0]=[str(D),str(D/'tests'),str(C),str(C/'tests')]
if sys.flags.optimize:raise RuntimeError('Optimized domain verification is forbidden')
from cakood.p12_model import P12World,SceneContext,CurrentRig,PEOPLE,PREREQUISITES,COURTYARD,LIVING,KITCHEN,PORCH,SIDE
from cakood.p10_model import P10World,P10Context,TILE_IDS,PAPER_IDS,ORDER
from cakood.p09_model import P09World,P09Context
from cakood.p11_model import P11World,P11Context
from cakood.p13_model import P13World,P13Context,PREREQUISITES as REQ13
from cakood.p04_model import project_gate
from dependencies.p03_numeric_model import P03
from dependencies.p04_numeric_model import P04,Obj,Bunting
from cakood.verbal_contest import VerbalContests,Catalog,Phase,YIELD_EXCHANGE
from test_verbal_contest import bind_rescue_result
from codec import M,encode_world,decode_words
from verify_source import verify
verify()
from paired import PairedVM as VM,restore_words,MEASUREMENTS
N={'actions':0,'restores':0,'speaker_checks':0,'variants':[],'scenarios':[],'phases':[]}
def eq(a,b,label):
    if a!=b:raise AssertionError((label,a,b))
def yes(a,label):
    if not a:raise AssertionError(label)
def rejects(fn,label):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError: '+label)
def displayed(w,c,source):
    p=w.begin_presentation(c,source);yes(p.presentation_id,('No presentation',source,p.code))
    records=w.SOURCES if hasattr(w,'SOURCES') else {'direct_question':'P09.DIALOGUE.001','terms':'P09.DIALOGUE.002'}
    r=w.acknowledge_presentation(c,p.presentation_id,record_id=records[source]);eq(r.code,'presentation_acknowledged',source)
def read_contest(vc,rescue=None,expected=None,scene_check=None):
    texts=[]
    while (p:=vc.pending_text()) is not None:
        before=vc.save();presented=bind_rescue_result(vc,p,rescue)
        eq(vc.save(),before,'Presentation selector must not mutate owner')
        eq(presented.receipt,p.receipt,'Original real owner receipt')
        if p.unit_id in ('VC03.WIN.02','VC03.LOSS.02') and rescue is not None:
            variant=next(v for v in vc.catalog.speech_unit(p.unit_id)['finite_variants'] if v['variant_id']==expected)
            eq(presented.text,variant['text'],'Exact variant text')
            yes(('rescue_credit_variant',expected) in presented.bindings,'Exact variant binding')
            texts.append({'unit_id':p.unit_id,'variant':expected,'text':presented.text})
        if scene_check:scene_check()
        vc.acknowledge_text(presented.receipt)
    return texts
def prepare_contest():
    vc=VerbalContests(Catalog());vc.introduce('VC03',admitted=True);read_contest(vc)
    for pair in vc.catalog.eligible('VC03'):vc.present_lesson('VC03',pair);read_contest(vc)
    return vc
def fight(vc,win,check=None):
    vc.enter('VC03',7,admitted=True)
    if check:check()
    for _ in range(3):
        vc.begin_turn(vc.active.id)
        if check:check()
        read_contest(vc,scene_check=check)
        if check:check()
        a=vc.active;pair=a.deck[a.cursor]
        response=next(iter(vc.catalog.pairs[pair].accepted_response_ids)) if win else YIELD_EXCHANGE
        vc.choose_response(a.exchange_id,response)
        if check:check()
        vc.commit_response(a.exchange_id)
        if check:check()
        read_contest(vc,scene_check=check)
        if vc.active.phase==Phase.KO_PENDING:break
    vc.commit_ko(vc.active.outcome_id)
    if check:check()
    yes(vc.progress['VC03'].resolved,'Real committed outcome')
    yes(vc.active is not None,'Unread result must remain active')
def owners(ids,rescue_mode):
    p3=P03();p3.context(6,0,1,1);p3.look(37);p3.begin_credit();p3.select(1)
    p3.context(2,0,1,1);p3.collect(38);p3.context(6,0,1,1);p3.pad(38);p3.give_slate()
    eq(p3.inventory(),[35],'Original tile group');eq([p3.location(x) for x in (48,49,50)],[10,10,10],'Original units')
    flags=frozenset({'EVENING_STARTED','PLAN_AGREED'})
    p9=P09World();c9=P09Context('L07_CONSERVATORY',flags=flags)
    displayed(p9,c9,'direct_question');displayed(p9,c9,'terms');flags|=p9.flags
    eq(p9.terms_card_handoff['signed'],False,'Unsigned terms')
    p10=P10World();pocket=set(TILE_IDS)|{'grease_pencil','master_invitation'}
    c10=P10Context(LIVING,flags=flags,inventory=frozenset(pocket))
    p10.introduce(c10);displayed(p10,c10,'plan')
    if set(ids)&set(PAPER_IDS):p10.prepare_paper(c10)
    for cue,word in zip(ids,ORDER):p10.write(c10,cue,word)
    for i,cue in enumerate(ids):
        p10.place(replace(c10,room=COURTYARD,inventory=frozenset(pocket)),cue,i);pocket.discard(cue)
    yes(p10.ready,'Earned P10 readiness');first=p10.restored_at
    # A normal remove/replace continues a restored owner before the handoff.
    context=lambda:replace(c10,room=COURTYARD,inventory=frozenset(pocket))
    p10.remove(context(),0)
    if ids[0] in TILE_IDS:pocket.add(ids[0])
    p10.place(context(),ids[0],0);pocket.discard(ids[0]);eq(p10.restored_at,first,'Historical restored serial')
    eq(p10.cue_handoff['slots'],tuple(ids),'Live reusable handoff')
    gate=P04();gate.context(3,0,1,1);gate.topic(Obj.FELIX,1);gate.open_gate();gate.place_wedge()
    gate.context(3,0,1,0);gate.move_bunting(Bunting.HELD);gate.move_bunting(Bunting.HOOK);gate.recover_wedge()
    gate.context(3,0,1,1);gate.close_gate(1);gate.open_gate();yes(gate.tested and gate.validate(),'Actual P04 tested owner')
    if rescue_mode!='ordinary':gate.set_peg(1)
    flags|=p10.flags;c11=P11Context(SIDE,project_gate(gate),flags=flags);p11=P11World();p11.lift(c11)
    if rescue_mode=='both':
        gate.set_peg(0);c11=replace(c11,gate=project_gate(gate))
    if rescue_mode!='pre_engaged':
        p11.request_peg(c11);request=p11.pending_peg_request_id;yes(request,'Genuine peg request')
        gate.set_peg(1);c11=replace(c11,gate=project_gate(gate));p11.acknowledge_peg(c11,request)
    p11.release_catch(c11);p11.pull_handle(c11);p11.stage_display(c11);displayed(p11,c11,'sincere')
    yes(p11.contest_eligible,'Complete protected rescue')
    variant='pre_engaged' if rescue_mode=='pre_engaged' else 'ordinary'
    eq(p11.rescue_credit_variant,variant,'Priority from actual serials')
    if rescue_mode=='both':yes(p11.peg_ack_at>0 and p11.advance_peg_at>0,'Both serials genuinely earned')
    request=p11.request_contest(c11);ev=request.events[0]
    eq((ev.payload['peg_ack_at'],ev.payload['advance_peg_at']),(p11.peg_ack_at,p11.advance_peg_at),'Request-time serial facts')
    snapshot=P11World.load(p11.save(),context=c11)
    p11.acknowledge_contest_request(c11,p11.pending_contest_request_id)
    vc=prepare_contest();c=SceneContext(COURTYARD,flags=flags|p11.flags,inventory=frozenset(pocket),npc_locations=tuple((p,COURTYARD) for p in PEOPLE[1:]),rig=CurrentRig(COURTYARD,True,'MIC',True),contests=vc)
    return p3,p9,p10,gate,p11,snapshot,vc,c,variant
class Pair:
    def __init__(self):self.w=P12World();self.v=VM();self.epoch=100
    def project(self,c):
        self.epoch+=1;rooms=dict(c.npc_locations)
        args=[M['rooms'][c.room],int(c.on_apron),*[int(f in c.flags) for f in ('EVENING_STARTED','CUES_RESTORED','DISPLAY_STAGED','HELP_ACCEPTED')],M['rooms'][c.rig.location],int(c.rig.connected),int(c.rig.source=='MIC'),int(c.rig.facing_inward),int(c.contest_active),int(c.resolved('VC03')),*[M['rooms'][rooms[p]] if p in rooms else -1 for p in PEOPLE[1:]],self.epoch]
        eq(self.v.call('p12Context',*args),1,'Projection')
        for obj in c.inventory:eq(self.v.call('p12ContextItem',M['objects'].get(obj,32767)),1,'Held item')
    def match(self,r):
        N['actions']+=1
        eq(self.v.persistent(),encode_world(self.w),'Persistent source/model equivalence')
        eq(self.v.p['p12Code'],M['codes'][r.code],'Source/model result')
        eq(tuple(self.v.call('p12Line',i) for i in range(self.v.p['p12LineCount'])),tuple(M['line_ids'][s] for s in r.line_ids),'Canonical records')
        eq(tuple(self.v.call('p12Unit',i) for i in range(self.v.p['p12UnitCount'])),tuple(M['speech_unit_ids'][s] for s in r.speech_unit_ids),'Canonical units')
        eq(tuple(self.v.call('p12Event',i) for i in range(self.v.p['p12EventCount'])),tuple(M['events'][e.id] for e in r.events),'Events')
        return r
    def call(self,c,model,source,*args,native=None):
        self.project(c);r=getattr(self.w,model)(c,*args);self.v.call(source,*(args if native is None else native));return self.match(r)
    def start(self,c,rack):
        args=(M['objects'][rack['rack_id']],M['rooms'][rack['location']],*divmod(rack['first_restored_serial'],32768),*[M['objects'][s] for s in rack['slots']],*[M['words'][s] for s in rack['words']])
        return self.call(c,'start','p12Handoff',rack,native=args)
    def begin(self,c,s):return self.call(c,'begin_presentation','p12Begin',s,native=(M['sources'][s],))
    def ack(self,c,s,tokens=None):
        self.project(c);p=self.w.presentations[s];sid=M['sources'][s];self.v.call('p12Resume',sid)
        if tokens is None:r=self.w.acknowledge_presentation(c,self.w._handle(s),record_id=self.w.SOURCES[s]);record=M['line_ids'][self.w.SOURCES[s]];first=last=0
        else:r=self.w.acknowledge_presentation(c,self.w._handle(s),speech_unit_ids=tokens);record=0;first=M['speech_unit_ids'][tokens[0]];last=M['speech_unit_ids'][tokens[-1]]
        self.v.call('p12Acknowledge',sid,*divmod(p.serial,32768),self.epoch,record,first,last);return self.match(r)
    def restore(self,c):
        before=self.w.save();old={s:self.w._handle(s) for s in self.w.presentations}
        words=list(self.v.persistent().values());eq(decode_words(words),before,'Codec roundtrip')
        self.w=P12World.load(before,context=c);self.v=restore_words(words);eq(self.w.save(),before,'Save continuity')
        eq(self.v.persistent(),encode_world(self.w),'Restored source continuity')
        for s,handle in old.items():eq(self.w.acknowledge_presentation(c,handle,record_id=self.w.SOURCES[s]).code,'stale_presentation','Old Python callback invalid')
        N['restores']+=1
    def show(self,c,s,restore=True):
        self.begin(c,s);tokens=self.w._tokens(s)
        if s=='diagram':self.ack(c,s)
        else:
            for token in tokens:
                self.ack(c,s,(token,))
                if restore:self.restore(c)
        yes(self.w._complete(s),'Complete source '+s)
    def nochange(self,c,model,source,*args,native=None,code=None):
        before=self.w.save();r=self.call(c,model,source,*args,native=native);eq(self.w.save(),before,'Nonmutating rejected action')
        if code:eq(r.code,code,'Expected block')
        return r
def probe_scenario(ids,mode,win,index):
    p3,p9,p10,gate,p11,snapshot,vc,c,variant=owners(ids,mode)
    pair=Pair();pair.start(c,p10.cue_handoff);apron=replace(c,on_apron=True)
    pair.nochange(c,'rotate_rack','p12Rotate',code='catch_required')
    pair.call(apron,'release_catch','p12ReleaseCatch');pair.nochange(c,'rotate_rack','p12Rotate',code='audience_side_observation_required')
    pair.show(apron,'audience_view' if index%2 else 'self_view');pair.call(c,'rotate_rack','p12Rotate')
    pair.call(c,'order_cards','p12Order',tuple(ids),native=tuple(M['objects'][x] for x in ids))
    pair.nochange(c,'choose_introduction','p12Choose','complete',native=(1,),code='vc03_resolution_required')
    phases=set()
    def blocked():
        phases.add(vc.active.phase.value)
        pair.nochange(c,'choose_introduction','p12Choose','complete',native=(1,),code='contest_active')
    fight(vc,win,blocked)
    eq(vc.progress['VC03'].won,win,'Win distinct from loss')
    captured=read_contest(vc,rescue=snapshot,expected=variant,scene_check=blocked)
    yes(vc.active is None,'DONE maps to idle');N['variants']+=captured;N['phases']+=sorted(phases)
    history=p11.save()
    # The opposite-result rematch retains the original cooperative rescue account.
    fight(vc,not win,blocked);N['variants']+=read_contest(vc,rescue=snapshot,expected=variant,scene_check=blocked)
    eq(p11.save(),history,'Rematch cannot rewrite rescue');yes(vc.progress['VC03'].won,'Ever won distinct from last loss')
    frozen=(copy.deepcopy(vars(p3)),p9.save(),p10.save(),gate.save(),p11.save(),vc.save())
    pair.nochange(c,'choose_introduction','p12Choose','partners',native=(3,),code='incomplete_introduction')
    pair.nochange(c,'choose_introduction','p12Choose','partnerships',native=(2,),code='incomplete_introduction')
    pair.begin(c,'introduction');tokens=pair.w._tokens('introduction')
    pair.ack(c,'introduction',tokens[:3]);pair.restore(c)
    for rig,code in [(replace(c.rig,connected=False),'microphone_unplugged'),(replace(c.rig,source='TAPE'),'selector_tape'),(replace(c.rig,facing_inward=False),'speaker_not_facing_inward'),(replace(c.rig,location=LIVING),'pa_not_present')]:
        bad=replace(c,rig=rig);before=pair.w.save();eq(pair.ack(bad,'introduction',tokens[3:4]).code,code,'Live PA receipt gate');eq(pair.w.save(),before,'No receipt while PA invalid')
    for token in tokens[3:]:pair.ack(c,'introduction',(token,));pair.restore(c)
    yes(not pair.w.ready,'Receipts require separate introduction commit')
    pair.call(c,'commit_introduction','p12CommitIntroduction');yes(not pair.w.welcome_cleared,'Intro does not finish cleanup')
    pair.nochange(c,'finish_welcome','p12FinishWelcome',code='cleanup_text_required')
    pot={'object_id':'hotpot_pot','room':KITCHEN,'lid_closed':True,'portions':8,'portion_kind':'tasting','includes_jackie':True}
    p13=P13World()
    def p13_attempt():
        cc=P13Context(COURTYARD,flags=REQ13,npc_locations=c.npc_locations,rig=c.rig,contests=vc,gate=project_gate(gate),welcome_cleared=pair.w.welcome_cleared)
        return p13.start(cc,pot,p11.display_handoff)
    eq(p13_attempt().code,'p12_collection_handoff_required','Real P13 intro barrier')
    pair.call(c,'release_confetti','p12ReleaseConfetti');pair.begin(c,'confetti')
    pair.ack(c,'confetti',pair.w._tokens('confetti')[:-1]);pair.restore(c)
    pair.nochange(c,'begin_presentation','p12Begin','cleanup',native=(M['sources']['cleanup'],),code='confetti_scene_pending')
    eq(p13_attempt().code,'p12_collection_handoff_required','Real P13 confetti prefix barrier')
    pair.ack(c,'confetti',pair.w._tokens('confetti')[-1:]);pair.show(c,'cleanup');pair.restore(c)
    eq(p13_attempt().code,'p12_collection_handoff_required','Real P13 requires collection event')
    r=pair.call(c,'finish_welcome','p12FinishWelcome');eq(r.events[0].payload['destinations'],{'bunny':KITCHEN,'frankie':LIVING,'rita':SIDE,'felix':SIDE,'vivian':SIDE,'milo':PORCH},'Authored departures')
    yes(r.events[0].payload['panel_covered'],'Covered panel retained');pair.restore(c)
    eq(p13_attempt().code,'deliveries_started','Real P13 entry after collection')
    pair.nochange(c,'finish_welcome','p12FinishWelcome',code='collection_already_started')
    eq((copy.deepcopy(vars(p3)),p9.save(),p10.save(),gate.save(),p11.save(),vc.save()),frozen,'P12 cannot mutate accepted owners')
    eq(pair.w.reserved_external_objects,frozenset(('cue_rack',*ids)),'Exact physical ownership projection')
    yes(not pair.w.flags&{'DISPLAY_REVEALED','GAME_COMPLETE','VC03_WON'},'No unrelated grants')
    N['scenarios'].append({'material':list(ids),'rescue':mode,'first_win':win,'variant':variant,'final_collection':pair.w.collection_at,'result':'PASS'})
def speaker_and_start_probes():
    _,_,p10,_,p11,snapshot,vc,c,variant=owners(TILE_IDS,'ordinary')
    fight(vc,False);read_contest(vc,rescue=snapshot,expected=variant)
    # The original method executes on the reconstructed class only.
    held=replace(c,inventory=c.inventory|{'cue_rack'});old=P12World();eq(old._literal_start(held,p10.cue_handoff).code,'rack_rehung','Literal omission contrast')
    fixed=Pair();before=fixed.w.save();rejects(lambda:fixed.start(held,p10.cue_handoff),'held rack');eq(fixed.w.save(),before,'Atomic held-rack rejection')
    fixed.project(held);h=p10.cue_handoff
    fixed.v.call('p12Handoff',M['objects']['cue_rack'],M['rooms'][COURTYARD],*divmod(h['first_restored_serial'],32768),*[M['objects'][x] for x in h['slots']],*[M['words'][x] for x in h['words']])
    eq(fixed.v.p['p12Code'],M['codes']['invalid_context'],'SCI held rack contrast')
    fixed.start(c,h);before=fixed.w.save();eq(fixed.w.start(held,{}).code,'already_rehung','Original repeat precedence');eq(fixed.w.save(),before,'Repeat no mutation')
    # Incomplete owners with both facts zero cannot select rescue result wording.
    again=prepare_contest();fight(again,False)
    while again.pending_text().unit_id!='VC03.LOSS.02':again.acknowledge_text(again.pending_text().receipt)
    rejects(lambda:bind_rescue_result(again,again.pending_text(),P11World()),'zero/zero incomplete rescue')
    pair=Pair();pair.start(c,h);a=replace(c,on_apron=True)
    stages={}
    for s in ('opening','rack','diagram','edge','audience_view','self_view','catch','rehearsal'):stages[s]=pair.w.save()
    pair.show(a,'self_view');pair.call(a,'release_catch','p12ReleaseCatch');pair.call(c,'rotate_rack','p12Rotate');pair.call(c,'order_cards','p12Order',TILE_IDS,native=tuple(M['objects'][x] for x in TILE_IDS));stages['introduction']=pair.w.save()
    pair.show(c,'introduction');pair.call(c,'commit_introduction','p12CommitIntroduction');pair.call(c,'release_confetti','p12ReleaseConfetti');stages['confetti']=pair.w.save();pair.show(c,'confetti');stages['cleanup']=pair.w.save()
    for source,save in stages.items():
        context=a if source in ('audience_view','self_view','catch','rehearsal') else c
        for token in P12World()._tokens(source):
            speaker=P12World.SPEAKERS.get(token)
            if speaker not in PEOPLE[1:]:continue
            w=P12World.load(save);p=w.begin_presentation(context,source);tokens=w._tokens(source);index=tokens.index(token)
            if index:w.acknowledge_presentation(context,p.presentation_id,speech_unit_ids=tokens[:index])
            away=replace(context,npc_locations=tuple((who,LIVING if who==speaker else room) for who,room in context.npc_locations));before=w.save()
            eq(w.acknowledge_presentation(away,p.presentation_id,speech_unit_ids=(token,)).code,'speaker_absent','Actual source speaker recheck');eq(w.save(),before,'Absent speaker no receipt')
            eq(w.acknowledge_presentation(context,p.presentation_id,speech_unit_ids=(token,)).code,'presentation_acknowledged','Returning speaker resumes');N['speaker_checks']+=1
    before=pair.w.save();pair.w.audio_finished();pair.w.hint(c,1);pair.w.journal_records();pair.w.journal_units();eq(pair.w.save(),before,'Pure calls grant nothing')
    before=pair.w.save();handle=pair.w._handle('confetti');pair.w.cancel_presentation(handle);eq(pair.w.save(),before,'Cancellation preserves receipts');eq(pair.w.acknowledge_presentation(c,handle,record_id=pair.w.SOURCES['confetti']).code,'stale_presentation','Cancellation invalidates handle')
def main():
    for i,(ids,mode,win) in enumerate(itertools.product((TILE_IDS,PAPER_IDS,(TILE_IDS[2],PAPER_IDS[0],TILE_IDS[0])),('ordinary','pre_engaged','both'),(False,True))):
        probe_scenario(ids,mode,win,i);print('PASS scenario',i,mode,win,flush=True)
    speaker_and_start_probes();N['phases']=sorted(set(N['phases']));N.update(status='PASS',optimized=sys.flags.optimize,paired=MEASUREMENTS)
    (R/'evidence'/('joined-gameplay.json')).write_text(json.dumps(N,indent=2)+'\n')
    print(json.dumps({k:v for k,v in N.items() if k not in ('variants','scenarios')},indent=2))
if __name__=='__main__':
    try:main()
    except Exception:
        (R/'evidence'/('joined-gameplay-failure.json')).write_text(json.dumps(N,indent=2)+'\n');raise
