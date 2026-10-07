"""Editable independent Python P03 model, reconstructed 2026-10-06.

Numeric identities follow the delivered domain ABI; final wording is supplied
by the immutable editorial catalog, not duplicated or invented here. Host must
hold source reads behind actual visible-page receipts before calling look/talk.
"""
from dataclasses import dataclass,field
from enum import IntEnum

class Code(IntEnum):
    OFFSCREEN=1; PLAN_REQUIRED=2; OBSERVED=3; INSPECT_STATE=4; SERVICE_READY=5
    SERVICE_RECAP=6; INTRODUCED=7; REVEAL_NOT_OFFERED=8; REVEAL_PROTECTED=9
    UNHELPFUL=10; ALREADY_HELD=11; CLOTH_COLLECTED=12; ALREADY_PADDED=13
    ITEM_NOT_HELD=14; PAPER_NOT_PADDING=15; CARRIER_PADDED=16; PENCIL_REQUIRED=17
    CREDIT_OPEN=18; EDITOR_REQUIRED=19; NAME_EVIDENCE_REQUIRED=20
    CREDIT_UNCHANGED=21; CREDIT_WRITTEN=22; EDITOR_CLOSED=23
    GENERIC_CREDIT_REJECTED=24; CREDIT_REQUIRED=25; PADDING_REQUIRED=26
    CREDIT_APPROVED=27; HINT=28; INVALID_ARGUMENT=29; INVALID_CONTEXT=30
    INVALID_STATE=31; SERIAL_EXHAUSTED=32

BINDINGS={1:(1,),2:(3,4),3:(23,4),4:(4,),5:(6,),6:(8,9),7:(11,12),8:(11,27),9:(11,25),10:(14,),11:(16,),12:(18,),13:(19,),14:(20,),15:(21,),16:(22,),17:(26,),18:(25,),19:(28,),20:(29,),21:(30,),22:(31,35,34),23:(33,),24:(37,38),25:(39,),26:(40,),27:(41,),28:(42,)}
SERIAL_MAX=32768**2-1

@dataclass
class State:
    initialized:int=1
    towel:int=0
    napkin:int=0
    padding:int=0
    slate:int=0
    approved:int=0
    editor_open:int=0
    know_name:int=0
    ready:int=0
    observed:int=0
    hint_level:int=0
    revision:int=0
    intro:int=0
    complete:int=0
    promise:int=0

@dataclass
class Result:
    code:int=0
    lines:list[int]=field(default_factory=list)
    events:list[tuple[int,int]]=field(default_factory=list)
    revision:int=0

class P03:
    def __init__(self):
        self.state=State();self.result=Result();self.context_valid=0
        self.room=0;self.apron=0;self.plan=0;self.tools=0;self.held=set()
    def clear(self):self.result=Result()
    def context(self,room,apron,plan,tools=0):
        self.clear();self.context_valid=0
        if not (0<=room<=6 and apron in (0,1) and plan in (0,1) and 0<=tools<=7):
            self.result.code=Code.INVALID_CONTEXT;return 0
        self.room,self.apron,self.plan,self.tools=room,apron,plan,tools
        self.held={o for o,b in ((25,1),(24,2),(46,4)) if tools&b};self.context_valid=1;return 1
    def context_item(self,obj):
        if not self.context_valid:return 0
        if obj<1 or obj>50 or obj in (2,8,30) or 33<=obj<=45 or 47<=obj<=50:
            self.context_valid=0;self.clear();self.status(Code.INVALID_CONTEXT);return 0
        self.held.add(obj);self.tools|={25:1,24:2,46:4}.get(obj,0);return 1
    def validate(self):
        s=self.state
        if s.initialized!=1:return False
        if any(v not in (0,1,2) for v in (s.towel,s.napkin,s.padding,s.slate)):return False
        if any(v not in (0,1) for v in (s.approved,s.editor_open,s.know_name,s.ready)):return False
        if not 0<=s.observed<=63 or not 0<=s.hint_level<=3:return False
        if any(not 0<=v<=SERIAL_MAX for v in (s.revision,s.intro,s.complete,s.promise)):return False
        if (s.towel==2)!=(s.padding==1) or (s.napkin==2)!=(s.padding==2):return False
        if bool(s.know_name)!=bool(s.observed&15):return False
        if s.slate==1 and not s.know_name:return False
        if s.observed&8 and not s.slate:return False
        if s.approved and s.slate!=1:return False
        if bool(s.ready)!=bool(s.padding and s.approved) or s.ready and s.editor_open:return False
        if bool(s.intro)!=bool(s.observed&4) or bool(s.ready)!=bool(s.complete):return False
        if any(v>s.revision for v in (s.intro,s.complete,s.promise)):return False
        if s.ready and s.intro and s.complete<=s.intro:return False
        if s.promise and (not s.ready or s.promise<=s.complete):return False
        if s.ready and s.complete<6:return False
        minimum=s.observed.bit_count()+int(bool(s.towel))+int(bool(s.napkin))+int(bool(s.padding))+int(bool(s.slate))
        minimum+=int(bool(s.observed&8) and s.slate==1)+int(bool(s.editor_open or s.slate))+s.approved
        minimum+=int(bool(s.hint_level))+int(bool(s.promise))
        return s.revision>=minimum
    def validate_context(self):
        s=self.state
        if not self.context_valid or not self.validate():return False
        progressed=any((s.padding,s.editor_open,s.slate,s.hint_level,s.ready,s.intro,s.promise,s.towel==1,s.napkin==1))
        if progressed and not self.plan:return False
        return not (s.editor_open and (self.apron or self.room!=6 or not self.tools&1))
    def start(self,need_context=True):
        self.clear()
        if not self.validate():self.result.code=Code.INVALID_STATE;return False
        if need_context and not self.context_valid:self.result.code=Code.INVALID_CONTEXT;return False
        return True
    def status(self,code,binding=0):
        self.result.code=int(code);self.result.lines.extend(BINDINGS.get(binding,()));return int(code)
    def can_commit(self):
        if self.state.revision==SERIAL_MAX:self.result.code=Code.SERIAL_EXHAUSTED;return False
        return True
    def commit(self,code,binding,event,arg=0,check_ready=False):
        s=self.state;s.revision+=1;self.result.revision=s.revision
        self.status(code,binding);self.result.events.append((event,arg))
        if event==2:s.intro=s.revision
        if event==11:s.promise=s.revision
        if check_ready and s.padding and s.approved and not s.ready:
            s.ready=1;s.editor_open=0;s.complete=s.revision
            self.result.lines.extend(BINDINGS[22]);self.result.events.append((10,s.padding))
        return int(code)
    def location(self,obj):
        s=self.state
        if obj in (38,39):return {0:11,1:10,2:12}[s.towel if obj==39 else s.napkin]
        if obj in (34,36,40,33,47):return 13 if s.ready else 6
        if obj in (35,48,49,50):return 10 if s.ready else 14
        if obj in (30,37,42,41):return 6
        if obj in (44,45,43):return 2
        if obj in (2,8):return 1
        return -1
    def reachable(self,obj):
        if not self.context_valid or self.apron:return False
        loc=self.location(obj)
        if loc==-1:return obj in self.held
        return loc in (10,self.room) or loc in (11,13) and self.room==2
    def guard(self,obj,target=0,plan=True):
        if self.apron:self.result.code=Code.OFFSCREEN;return False
        if plan and not self.plan:self.result.code=Code.PLAN_REQUIRED;return False
        if not self.reachable(obj) or target and not self.reachable(target):self.result.code=Code.OFFSCREEN;return False
        return True
    def observe(self,bit):
        if self.state.observed&bit:return 0
        if not self.can_commit():return -1
        self.state.observed|=bit
        if bit&15:self.state.know_name=1
        return 1
    def look(self,obj):
        if not self.start() or not self.guard(obj,plan=False):return self.result.code
        s=self.state
        bit,binding={34:(16,3 if s.padding else 2),33:(16,4),36:(1,5),47:(1,5),37:(2,6),40:(0,{0:7,1:8,2:9}[s.slate]),42:(32,24),41:(32,24),35:(0,23),39:(0,10),38:(0,11),44:(0,12 if not s.towel and not s.napkin else 0)}.get(obj,(0,0))
        if bit:
            observed=self.observe(bit)
            if observed<0:return self.result.code
            if observed:return self.commit(Code.OBSERVED,binding,1,bit)
        return self.status(Code.OBSERVED if binding else Code.INSPECT_STATE,binding)
    def talk(self,actor,topic):
        if not self.start():return self.result.code
        if topic not in (1,2,3):return self.status(Code.INVALID_ARGUMENT)
        if not self.guard(actor):return self.result.code
        s=self.state
        if actor==30 and topic in (1,2):
            if s.intro or s.ready:return self.status(Code.SERVICE_READY if s.ready else Code.SERVICE_RECAP)
            if not self.can_commit():return self.result.code
            self.observe(4);return self.commit(Code.INTRODUCED,1,2)
        if actor in (2,8) and topic==3:
            if not s.ready:return self.status(Code.REVEAL_NOT_OFFERED)
            if s.promise:return self.status(Code.REVEAL_PROTECTED)
            if not self.can_commit():return self.result.code
            return self.commit(Code.REVEAL_PROTECTED,25,11)
        return self.status(Code.UNHELPFUL)
    def collect(self,obj):
        if not self.start():return self.result.code
        if obj not in (38,39):return self.status(Code.INVALID_ARGUMENT)
        if not self.guard(obj):return self.result.code
        name='towel' if obj==39 else 'napkin'
        if getattr(self.state,name)==1:return self.status(Code.ALREADY_HELD)
        if not self.can_commit():return self.result.code
        setattr(self.state,name,1);return self.commit(Code.CLOTH_COLLECTED,13 if obj==39 else 14,3,obj)
    def pad(self,obj):
        if not self.start():return self.result.code
        if obj not in (39,38,46,24):return self.status(Code.INVALID_ARGUMENT)
        if not self.guard(34):return self.result.code
        s=self.state
        if s.padding:return self.status(Code.ALREADY_PADDED,3)
        if not (obj==39 and s.towel==1 or obj==38 and s.napkin==1 or obj in self.held):return self.status(Code.ITEM_NOT_HELD)
        if obj in (46,24):return self.status(Code.PAPER_NOT_PADDING,19 if obj==46 else 20)
        if not self.can_commit():return self.result.code
        s.padding=1 if obj==39 else 2
        if obj==39:s.towel=2
        else:s.napkin=2
        return self.commit(Code.CARRIER_PADDED,15 if obj==39 else 16,4,obj,True)
    def begin_credit(self):
        if not self.start() or not self.guard(40):return self.result.code
        if not self.tools&1:return self.status(Code.PENCIL_REQUIRED)
        s=self.state
        if s.ready:return self.status(Code.SERVICE_READY,8)
        if s.editor_open:return self.status(Code.CREDIT_OPEN)
        if not self.can_commit():return self.result.code
        s.editor_open=1;return self.commit(Code.CREDIT_OPEN,0,5)
    def choices(self):
        if not self.context_valid or not self.state.editor_open or self.apron or self.room!=6 or not self.plan or not self.tools&1:return 0
        return 3 if self.state.know_name else 2
    def select(self,choice):
        if not self.start():return self.result.code
        if choice not in (1,2):return self.status(Code.INVALID_ARGUMENT)
        if not self.guard(40):return self.result.code
        if not self.tools&1:return self.status(Code.PENCIL_REQUIRED)
        s=self.state
        if not s.editor_open:return self.status(Code.EDITOR_REQUIRED)
        if choice==1 and not s.know_name:return self.status(Code.NAME_EVIDENCE_REQUIRED)
        if s.slate==choice:return self.status(Code.CREDIT_UNCHANGED)
        if not self.can_commit():return self.result.code
        s.slate=choice;s.approved=0;return self.commit(Code.CREDIT_WRITTEN,17 if choice==1 else 18,6,choice)
    def cancel_credit(self):
        if not self.start(False):return self.result.code
        if not self.state.editor_open:return self.status(Code.EDITOR_CLOSED)
        if not self.can_commit():return self.result.code
        self.state.editor_open=0;return self.commit(Code.EDITOR_CLOSED,0,7)
    def give_slate(self):
        if not self.start() or not self.guard(40,30):return self.result.code
        s=self.state
        if s.slate==2:
            observed=self.observe(8)
            if observed<0:return self.result.code
            if observed:return self.commit(Code.GENERIC_CREDIT_REJECTED,21,1,8)
            return self.status(Code.GENERIC_CREDIT_REJECTED,21)
        if s.slate!=1:return self.status(Code.CREDIT_REQUIRED)
        if s.approved:return self.status(Code.PADDING_REQUIRED)
        if not self.can_commit():return self.result.code
        s.approved=1;s.editor_open=0;return self.commit(Code.CREDIT_APPROVED,0,8,0,True)
    def hint(self,level=0):
        if not self.start():return self.result.code
        if level not in (0,1,2,3):return self.status(Code.INVALID_ARGUMENT)
        if not self.plan:return self.status(Code.PLAN_REQUIRED)
        s=self.state
        if s.ready:return self.status(Code.SERVICE_READY)
        desired=level or min(3,s.hint_level+1);binding=25+desired
        if desired<=s.hint_level:return self.status(Code.HINT,binding)
        if not self.can_commit():return self.result.code
        s.hint_level=desired;return self.commit(Code.HINT,binding,9,desired)
    def act(self,verb,obj,target=0):
        if not self.start():return self.result.code
        if not 1<=verb<=9:return self.status(Code.INVALID_ARGUMENT)
        if not self.guard(obj,target,verb!=5):return self.result.code
        if verb==5 and not target:return self.look(obj)
        if verb==6 and not target and obj==30:return self.talk(obj,1)
        if verb==4 and not target and obj in (39,38):return self.collect(obj)
        if verb==7 and target==34 and obj in (39,38,24,46):return self.pad(obj)
        if verb==7 and obj==25 and target==40:return self.begin_credit()
        if verb==1 and obj==40 and target==30:return self.give_slate()
        return self.status(Code.UNHELPFUL)
    def inventory(self):
        s=self.state
        return ([39] if s.towel==1 else [])+([38] if s.napkin==1 else [])+([35] if s.ready else [])
    def after_restore(self):
        self.clear();self.context_valid=0;return int(self.validate())
    def snapshot(self):
        s=self.state;r=self.result
        p={f'p03{k}':v for k,v in {'Initialized':s.initialized,'Towel':s.towel,'Napkin':s.napkin,'Padding':s.padding,'Slate':s.slate,'Approved':s.approved,'Open':s.editor_open,'KnowName':s.know_name,'Ready':s.ready,'Observed':s.observed,'HintLevel':s.hint_level,'ContextValid':self.context_valid,'Room':self.room,'Apron':self.apron,'Plan':self.plan,'Tools':self.tools,'Code':r.code,'LineCount':len(r.lines),'EventCount':len(r.events)}.items()}
        for prefix,value in [('Revision',s.revision),('Intro',s.intro),('Complete',s.complete),('Promise',s.promise),('Result',r.revision)]:p['p03'+prefix+'Hi'],p['p03'+prefix+'Lo']=divmod(value,32768)
        return p
