"""Independent readable P04 reconstruction, 2026-10-06. Not a native proof.

The state machine is expressed in ordinary Python, not evaluated/transpiled SCI.
Numeric identifiers follow the recovered ABI. Save receipts are 30-bit integers
internally and exactly fourteen signed-word-safe properties on the boundary.
The caller owns external wedge inventory and refreshes context after a commit.
Observation calls require the host's actual source-page presentation receipts.
"""
from dataclasses import dataclass, field, fields
from enum import IntEnum
from collections.abc import Mapping

BASE = 32768
SERIAL_MAX = BASE * BASE - 1

class Code(IntEnum):
    ALREADY_CLOSED=1; ALREADY_HELD=2; ALREADY_HELD_BY_PEG=3; ALREADY_OPEN=4
    ALREADY_WEDGED=5; BUNTING_CAUGHT=6; BUNTING_MOVED=7; BUNTING_UNCHANGED=8
    CANCELLED=9; FORCE_REFUSED=10; FREE_BUNTING_REQUIRED=11; GATE_CHECKED=12
    GATE_CLOSED=13; GATE_OPEN=14; GATE_WEDGED=15; HINT=16; HOLD_GATE_REQUIRED=17
    HOOK_REQUIRED=18; INSPECT_STATE=19; INSTRUCTIONS=20; INTRODUCED=21
    INVALID_ARGUMENT=22; INVALID_CONTEXT=23; INVALID_STATE=24
    LEAVE_REPAIRED_PARTS=25; OBSERVED=26; OFFSCREEN=27; OPEN_REQUIRED=28
    PEG_BLOCKS_CLOSE=29; PEG_ENGAGED=30; PEG_RELEASED=31; PEG_UNCHANGED=32
    PLAN_REQUIRED=33; RECOVER_WEDGE_REQUIRED=34; SERIAL_EXHAUSTED=35
    TEST_REQUIRED=36; UNHELPFUL=37; WEDGE=38; WEDGE_BLOCKS_CLOSE=39
    WEDGE_BLOCKS_TEST=40; WEDGE_ELSEWHERE=41; WEDGE_RECOVERED=42; WEDGE_REQUIRED=43

class Obj(IntEnum):
    WEDGE=4; ALIGNED_HINGES=51; CIRCULATION_BOARD=52; CIRCULATION_PLAN=53
    FELIX=54; FIXED_HOOK=55; HOLD_OPEN_PEG=56; JACK=57; LATCH_ARM=58
    SCREWDRIVER=59; SIDE_GATE=60; VIVIAN=61; WELCOME_BUNTING=62

class Verb(IntEnum):
    GIVE=1; OPEN=2; CLOSE=3; PICK_UP=4; LOOK=5; TALK=6; USE=7; PUSH=8; PULL=9

class Event(IntEnum):
    OBSERVE=1; INTRO=2; GATE_OPEN=3; WEDGE_PLACED=4; WEDGE_RECOVERED=5
    BUNTING_MOVED=6; COMPLETE=7; GATE_CLOSE=8; PEG_CHANGED=9; HINT=10

class Gate(IntEnum):
    RESTING=0; OPEN=1; CLOSED=2
    CAUGHT=RESTING  # Compatibility alias for the initial reconstruction label

class Bunting(IntEnum):
    LATCH=0; HELD=1; HOOK=2

BINDINGS = {
    1:(1,), 2:(3,), 3:(5,), 4:(7,), 5:(9,), 6:(11,12), 7:(14,),
    8:(16,), 9:(17,), 10:(18,), 11:(19,), 12:(20,), 13:(21,), 14:(22,),
    15:(23,), 16:(24,), 17:(25,), 18:(26,27,33), 19:(29,30), 20:(31,),
    21:(32,), 22:(34,), 23:(35,), 24:(36,),
}
# Reconstructed allowlists from all recovered observation writers and the
# campaign identity contract; the missing original manifest did not print them.
LATCH_SOURCES = frozenset((3,7,9,17,20,23,24))
HOOK_SOURCES = frozenset((11,17,21))
FIXED_OBJECTS = frozenset((51,52,53,55,56,58,60))
OWNED_ITEMS = frozenset((62,))
FIXED_NPCS = frozenset((2,8,28,29,30,54,57,61))
CONTEXT_FORBIDDEN = FIXED_OBJECTS | OWNED_ITEMS | FIXED_NPCS
PERSISTED_SIMPLE = {
    'p04Initialized':'initialized', 'p04Gate':'gate', 'p04Bunting':'bunting',
    'p04Wedge':'wedge', 'p04Peg':'peg', 'p04LatchSource':'latch_source',
    'p04HookSource':'hook_source', 'p04HintLevel':'hint_level',
}
PERSISTED_FIELDS = tuple(PERSISTED_SIMPLE) + tuple(
    'p04'+name+limb for name in ('Revision','Intro','Complete') for limb in ('Hi','Lo'))

@dataclass
class State:
    initialized:int=1
    gate:int=0
    bunting:int=0
    wedge:int=0
    peg:int=0
    latch_source:int=0
    hook_source:int=0
    hint_level:int=0
    revision:int=0
    intro:int=0
    complete:int=0

@dataclass
class Result:
    code:int=0
    lines:list[int]=field(default_factory=list)
    events:list[tuple[int,int,int]]=field(default_factory=list)
    revision:int=0

class P04:
    def __init__(self):
        self.state=State()
        self.result=Result()
        self.context_valid=0
        self.room=self.apron=self.plan=0
        self.held=set()

    def clear(self):
        self.result=Result()
        return 1

    def init(self):
        if self.state.initialized:return 0
        self.state.initialized=1
        self.clear()
        return 1

    def context(self,room,apron,plan,wedge_held=0):
        self.clear()
        self.context_valid=0
        if not (all(isinstance(x,int) for x in (room,apron,plan,wedge_held))
                and 0<=room<=6 and apron in (0,1) and plan in (0,1)
                and wedge_held in (0,1) and not (wedge_held and self.state.wedge)):
            self.result.code=Code.INVALID_CONTEXT
            return 0
        self.room,self.apron,self.plan=room,apron,plan
        self.held={int(Obj.WEDGE)} if wedge_held else set()
        self.context_valid=1
        return 1

    def context_item(self,obj):
        if not self.context_valid:return 0
        if (not isinstance(obj,int) or not 1<=obj<=62 or obj in CONTEXT_FORBIDDEN
                or obj==Obj.WEDGE and self.state.wedge):
            self.context_valid=0
            self.clear()
            self.result.code=Code.INVALID_CONTEXT
            return 0
        self.held.add(int(obj))
        return 1

    @property
    def tested(self):
        """Historical successful self-closing test, permanently latched."""
        return bool(self.state.complete)

    @property
    def peg_available(self):return self.tested

    @property
    def gate_open(self):return self.state.gate==Gate.OPEN

    @property
    def gate_navigable(self):
        """Physical open-gate traversal; never substitutes for test credit."""
        return self.gate_open

    @property
    def flags(self):
        return frozenset(('GATE_TESTED','HOLD_OPEN_AVAILABLE')) if self.tested else frozenset()

    def ready(self):return int(bool(self.state.complete))
    def know(self):return int(bool(self.state.latch_source and self.state.hook_source))

    def validate(self):
        s=self.state
        if any(not isinstance(getattr(s,f.name),int) for f in fields(State)):return False
        if s.initialized!=1 or s.gate not in (0,1,2) or s.bunting not in (0,1,2):return False
        if s.wedge not in (0,1) or s.peg not in (0,1) or not 0<=s.hint_level<=3:return False
        if any(not 0<=v<=SERIAL_MAX for v in (s.revision,s.intro,s.complete)):return False
        if s.latch_source not in LATCH_SOURCES|{0} or s.hook_source not in HOOK_SOURCES|{0}:return False
        # Exactly one support, always on an open gate; the tethered peg requires
        # the historical successful self-close receipt.
        if (s.wedge or s.peg) and s.gate!=Gate.OPEN:return False
        if s.wedge and s.peg or s.peg and not s.complete:return False
        if s.bunting!=Bunting.LATCH and not s.latch_source:return False
        if s.bunting==Bunting.HOOK and not s.hook_source:return False
        if (s.gate==Gate.RESTING and s.bunting!=Bunting.LATCH
                or s.gate==Gate.CLOSED and s.bunting==Bunting.LATCH):return False
        if (s.intro or s.complete) and not self.know():return False
        if s.intro>s.revision or s.complete>s.revision:return False
        if s.complete and (s.complete<6 or s.intro and s.complete<=s.intro):return False
        # Lower bounds reject impossible snapshots without pretending that a
        # coarse receipt proves the exact complete history.
        observations=int(bool(s.latch_source))+int(bool(s.hook_source) and s.hook_source!=s.latch_source)
        observations+=int(bool(s.intro) and 17 not in (s.latch_source,s.hook_source))
        moved={Bunting.LATCH:0,Bunting.HELD:3,Bunting.HOOK:4}[s.bunting]
        support=2 if s.wedge else int(s.gate!=Gate.RESTING)
        minimum=max(observations,moved,support)+int(bool(s.hint_level))
        if s.revision<minimum:return False
        if s.complete:
            support_after=2 if s.wedge or s.peg else 0
            moved_after={Bunting.LATCH:4,Bunting.HELD:3,Bunting.HOOK:0}[s.bunting]
            gate_after={Gate.RESTING:6,Gate.OPEN:1,Gate.CLOSED:0}[s.gate]
            if s.revision-s.complete<max(support_after,moved_after,gate_after):return False
        return True

    def validate_context(self):
        s=self.state
        if not self.context_valid or not self.validate() or s.wedge and Obj.WEDGE in self.held:return False
        progressed=any((s.intro,s.complete,s.hint_level,s.wedge,s.gate!=0,s.bunting!=0,
                        s.latch_source not in (0,3,7,9),s.hook_source not in (0,11)))
        return bool(self.plan or not progressed)

    def start(self,needs_context=True):
        self.clear()
        if not self.validate():
            self.result.code=Code.INVALID_STATE
            return False
        if needs_context and (not self.context_valid or self.state.wedge and Obj.WEDGE in self.held):
            self.result.code=Code.INVALID_CONTEXT
            return False
        return True

    def status(self,code,binding=0):
        self.result.code=int(code)
        for line in BINDINGS.get(binding,()):self.append_line(line)
        return int(code)

    def append_line(self,line):
        if not 1<=line<=36 or len(self.result.lines)>=8:return 0
        self.result.lines.append(int(line))
        return 1

    def bind(self,binding):
        for line in BINDINGS.get(binding,()):self.append_line(line)
        return len(self.result.lines)

    def line(self,index):return self.result.lines[index] if 0<=index<len(self.result.lines) else 0
    def event(self,index):return self.result.events[index][0] if 0<=index<len(self.result.events) else 0
    def event_arg(self,index):return self.result.events[index][1] if 0<=index<len(self.result.events) else 0
    def event_arg2(self,index):return self.result.events[index][2] if 0<=index<len(self.result.events) else 0

    def can_commit(self):
        if self.state.revision==SERIAL_MAX:
            self.result.code=Code.SERIAL_EXHAUSTED
            return False
        return True

    def commit(self,code,binding,event,arg=0,arg2=0):
        self.state.revision+=1
        self.result.revision=self.state.revision
        self.status(code,binding)
        self.result.events=[(int(event),int(arg),int(arg2))]
        if event==Event.INTRO:self.state.intro=self.state.revision
        if event==Event.COMPLETE:self.state.complete=self.state.revision
        return int(code)

    def location(self,obj):
        s=self.state
        if obj==Obj.WEDGE:return 11 if s.wedge else -1
        if obj==Obj.WELCOME_BUNTING:return (12,10,13)[s.bunting]
        if obj in (Obj.CIRCULATION_PLAN,Obj.CIRCULATION_BOARD):return 1 if s.complete else -1
        if obj in (Obj.SIDE_GATE,Obj.ALIGNED_HINGES,Obj.LATCH_ARM,Obj.FIXED_HOOK,Obj.HOLD_OPEN_PEG,Obj.FELIX):return 3
        return -1

    def reachable(self,obj):
        if not self.context_valid or self.apron or self.state.wedge and Obj.WEDGE in self.held:return False
        loc=self.location(obj)
        if loc==-1:return bool(isinstance(obj,int) and 1<=obj<=62 and obj in self.held)
        return loc in (10,self.room) or loc in (11,12,13) and self.room==3

    def guard(self,obj,target=0,preparation=True):
        if self.apron:self.result.code=Code.OFFSCREEN
        elif preparation and not self.plan:self.result.code=Code.PLAN_REQUIRED
        elif not self.reachable(obj) or target and not self.reachable(target):self.result.code=Code.OFFSCREEN
        else:return True
        return False

    def observe(self,latch=0,hook=0):
        s=self.state
        if not (latch and not s.latch_source or hook and not s.hook_source):return 0
        if not self.can_commit():return -1
        if latch and not s.latch_source:s.latch_source=int(latch)
        if hook and not s.hook_source:s.hook_source=int(hook)
        return 1

    def look(self,obj):
        if not self.start() or not self.guard(obj,preparation=False):return self.result.code
        s=self.state
        binding=latch=hook=0
        if s.bunting==Bunting.LATCH:
            binding,latch={Obj.SIDE_GATE:(2,3),Obj.LATCH_ARM:(4,7),Obj.WELCOME_BUNTING:(5,9)}.get(obj,(0,0))
        elif obj==Obj.SIDE_GATE and s.complete and s.bunting==Bunting.HOOK:binding=20
        if obj==Obj.FIXED_HOOK:binding,hook=6,11
        elif obj==Obj.ALIGNED_HINGES:binding=3
        elif obj==Obj.HOLD_OPEN_PEG:binding=21 if s.complete else 7
        elif obj==Obj.WEDGE:binding=8
        elif obj in (Obj.CIRCULATION_PLAN,Obj.CIRCULATION_BOARD):binding=19
        changed=self.observe(latch,hook)
        if changed<0:return self.result.code
        if changed:return self.commit(Code.OBSERVED,binding,Event.OBSERVE)
        return self.status(Code.OBSERVED if binding else Code.INSPECT_STATE,binding)

    def topic(self,actor,topic):
        if not self.start():return self.result.code
        if topic not in (1,2,3):return self.status(Code.INVALID_ARGUMENT)
        if not self.guard(actor):return self.result.code
        if actor!=Obj.FELIX:return self.status(Code.UNHELPFUL)
        s=self.state
        if s.complete:return self.status(Code.GATE_CHECKED,21)
        if s.bunting!=Bunting.LATCH:return self.status(Code.HOOK_REQUIRED if s.bunting==Bunting.HELD else Code.TEST_REQUIRED)
        introductory=topic<3 and not s.intro and not s.wedge
        if introductory and not self.can_commit():return self.result.code
        changed=self.observe(17,17)
        if changed<0:return self.result.code
        if introductory:
            s.gate=Gate.RESTING
            self.commit(Code.INTRODUCED,1,Event.INTRO)
            self.bind(9)
            return self.result.code
        if changed:return self.commit(Code.INSTRUCTIONS,9,Event.OBSERVE)
        return self.status(Code.INSTRUCTIONS,9)

    talk=topic

    def open_gate(self):
        if not self.start() or not self.guard(Obj.SIDE_GATE):return self.result.code
        if self.state.gate==Gate.OPEN:return self.status(Code.ALREADY_OPEN)
        if not self.can_commit():return self.result.code
        self.state.gate=Gate.OPEN
        return self.commit(Code.GATE_OPEN,10 if self.state.bunting==Bunting.LATCH else 0,Event.GATE_OPEN)

    def place_wedge(self):
        if not self.start() or not self.guard(Obj.SIDE_GATE):return self.result.code
        s=self.state
        if s.wedge:return self.status(Code.ALREADY_WEDGED)
        if Obj.WEDGE not in self.held:return self.status(Code.WEDGE_REQUIRED)
        if s.gate!=Gate.OPEN:return self.status(Code.OPEN_REQUIRED)
        if s.peg:return self.status(Code.ALREADY_HELD_BY_PEG)
        if not self.can_commit():return self.result.code
        s.wedge=1
        return self.commit(Code.GATE_WEDGED,11,Event.WEDGE_PLACED,Obj.WEDGE)

    def recover_wedge(self):
        if not self.start() or not self.guard(Obj.SIDE_GATE):return self.result.code
        if not self.state.wedge:return self.status(Code.ALREADY_HELD if Obj.WEDGE in self.held else Code.WEDGE_ELSEWHERE)
        if not self.can_commit():return self.result.code
        self.state.wedge=0
        return self.commit(Code.WEDGE_RECOVERED,14,Event.WEDGE_RECOVERED,Obj.WEDGE)

    def move_bunting(self,destination):
        if not self.start():return self.result.code
        if destination not in (0,1,2):return self.status(Code.INVALID_ARGUMENT)
        if not self.guard(Obj.SIDE_GATE,Obj.WELCOME_BUNTING):return self.result.code
        s=self.state
        if s.bunting==destination:return self.status(Code.BUNTING_UNCHANGED)
        if s.gate!=Gate.OPEN or not (s.wedge or s.peg):
            if s.bunting==Bunting.LATCH:
                changed=self.observe(17,17)
                if changed<0:return self.result.code
                if changed:return self.commit(Code.HOLD_GATE_REQUIRED,9,Event.OBSERVE)
                return self.status(Code.HOLD_GATE_REQUIRED,9)
            return self.status(Code.HOLD_GATE_REQUIRED)
        if s.bunting!=Bunting.HELD and destination!=Bunting.HELD:return self.status(Code.FREE_BUNTING_REQUIRED)
        if not self.can_commit():return self.result.code
        previous=s.bunting
        s.bunting=int(destination)
        binding=0
        if previous==Bunting.LATCH and destination==Bunting.HELD:
            binding=12
            if not s.latch_source:s.latch_source=20
        elif destination==Bunting.HOOK:
            binding=13
            if not s.hook_source:s.hook_source=21
        return self.commit(Code.BUNTING_MOVED,binding,Event.BUNTING_MOVED,previous,destination)

    def close_gate(self,test=0):
        if not self.start():return self.result.code
        if test not in (0,1):return self.status(Code.INVALID_ARGUMENT)
        if not self.guard(Obj.SIDE_GATE):return self.result.code
        s=self.state
        if s.wedge:return self.status(Code.WEDGE_BLOCKS_TEST if test else Code.WEDGE_BLOCKS_CLOSE,17)
        if s.peg:return self.status(Code.PEG_BLOCKS_CLOSE)
        if test and s.bunting!=Bunting.HOOK:return self.status(Code.BUNTING_CAUGHT if s.bunting==Bunting.LATCH else Code.HOOK_REQUIRED)
        if test and s.gate!=Gate.OPEN:return self.status(Code.OPEN_REQUIRED)
        position=Gate.RESTING if s.bunting==Bunting.LATCH else Gate.CLOSED
        if test and not s.complete:
            if not self.can_commit():return self.result.code
            s.gate=position
            return self.commit(Code.GATE_CHECKED,18,Event.COMPLETE)
        if s.gate==position:return self.status(Code.ALREADY_CLOSED)
        if not self.can_commit():return self.result.code
        s.gate=position
        return self.commit(Code.GATE_CLOSED,0,Event.GATE_CLOSE)

    def set_peg(self,engaged):
        if not self.start():return self.result.code
        if engaged not in (0,1):return self.status(Code.INVALID_ARGUMENT)
        if not self.guard(Obj.HOLD_OPEN_PEG):return self.result.code
        s=self.state
        if not s.complete:return self.status(Code.TEST_REQUIRED,7)
        if s.peg==engaged:return self.status(Code.PEG_UNCHANGED)
        if engaged and s.gate!=Gate.OPEN:return self.status(Code.OPEN_REQUIRED)
        if engaged and s.wedge:return self.status(Code.RECOVER_WEDGE_REQUIRED)
        if not self.can_commit():return self.result.code
        s.peg=int(engaged)
        return self.commit(Code.PEG_ENGAGED if engaged else Code.PEG_RELEASED,0,Event.PEG_CHANGED,engaged)

    def refuse_force(self,obj):
        if not self.start():return self.result.code
        if obj not in (Obj.ALIGNED_HINGES,Obj.LATCH_ARM):return self.status(Code.INVALID_ARGUMENT)
        if not self.guard(obj):return self.result.code
        if self.state.bunting!=Bunting.LATCH:return self.status(Code.LEAVE_REPAIRED_PARTS)
        binding,source=(15,23) if obj==Obj.ALIGNED_HINGES else (16,24)
        changed=self.observe(source,0)
        if changed<0:return self.result.code
        if changed:return self.commit(Code.FORCE_REFUSED,binding,Event.OBSERVE)
        return self.status(Code.FORCE_REFUSED,binding)

    def hint(self,level=0):
        if not self.start():return self.result.code
        if level not in (0,1,2,3):return self.status(Code.INVALID_ARGUMENT)
        if not self.plan:return self.status(Code.PLAN_REQUIRED)
        s=self.state
        if s.complete:return self.status(Code.GATE_CHECKED)
        requested=level or min(s.hint_level+1,3)
        binding=21+requested
        if requested<=s.hint_level:return self.status(Code.HINT,binding)
        if not self.can_commit():return self.result.code
        s.hint_level=int(requested)
        return self.commit(Code.HINT,binding,Event.HINT,requested)

    def cancel(self):
        if not self.start(False):return self.result.code
        return self.status(Code.CANCELLED)

    def act(self,verb,obj,target=0):
        if not self.start():return self.result.code
        if verb not in range(1,10):return self.status(Code.INVALID_ARGUMENT)
        if not self.guard(obj,target,verb!=Verb.LOOK):return self.result.code
        if verb==Verb.LOOK and not target:return self.look(obj)
        if verb==Verb.TALK and not target and obj==Obj.FELIX:return self.topic(obj,1)
        if obj==Obj.SIDE_GATE and not target:
            if verb==Verb.OPEN:return self.open_gate()
            if verb in (Verb.CLOSE,Verb.PUSH):return self.close_gate(int(verb==Verb.PUSH))
        if verb==Verb.USE and obj==Obj.WEDGE and target==Obj.SIDE_GATE:return self.place_wedge()
        if verb==Verb.PICK_UP and obj==Obj.WEDGE and not target:return self.recover_wedge()
        if obj==Obj.WELCOME_BUNTING:
            if verb==Verb.PULL and not target:return self.move_bunting(Bunting.HELD)
            if verb==Verb.USE and target in (Obj.FIXED_HOOK,Obj.LATCH_ARM):
                return self.move_bunting(Bunting.HOOK if target==Obj.FIXED_HOOK else Bunting.LATCH)
        if obj==Obj.HOLD_OPEN_PEG:
            if verb in (Verb.USE,Verb.PUSH) and target in (0,Obj.SIDE_GATE):return self.set_peg(1)
            if verb==Verb.PULL and not target:return self.set_peg(0)
        if obj in (Obj.ALIGNED_HINGES,Obj.LATCH_ARM) and verb in (Verb.PULL,Verb.PUSH,Verb.USE):return self.refuse_force(obj)
        return self.status(Code.UNHELPFUL)

    def inventory(self):return [int(Obj.WELCOME_BUNTING)] if self.state.bunting==Bunting.HELD else []
    def reserved(self):return [int(Obj.WEDGE)] if self.state.wedge else []
    def inventory_at(self,index):return self.inventory()[0] if index==0 and self.inventory() else 0
    def reserved_at(self,index):return self.reserved()[0] if index==0 and self.reserved() else 0

    def journal(self):
        sources=[]
        for source in (self.state.latch_source,self.state.hook_source):
            if source and source not in sources:sources.append(source)
        if self.state.complete:sources.append(30)
        return sources

    def journal_at(self,index):
        entries=self.journal()
        return entries[index] if 0<=index<len(entries) else 0

    def after_restore(self):
        self.clear()
        self.context_valid=0
        return int(self.validate())

    def persisted(self):
        out={prop:int(getattr(self.state,name)) for prop,name in PERSISTED_SIMPLE.items()}
        for name in ('Revision','Intro','Complete'):
            out['p04'+name+'Hi'],out['p04'+name+'Lo']=divmod(getattr(self.state,name.lower()),BASE)
        return out

    def save(self):
        """Return a new, JSON-compatible exact 14-property save; reject corruption."""
        if not self.validate():raise ValueError('Invalid P04 state cannot be saved')
        return self.persisted()

    def load(self,payload):
        """Atomically load an exact 14-property save and invalidate stale context.

        Invalid input raises ValueError without replacing the current world.
        Direct state corruption tests can use after_restore() to exercise the
        SCI fail-closed/no-repair behavior instead of this strict file boundary.
        """
        if not isinstance(payload,Mapping) or set(payload)!=set(PERSISTED_FIELDS):
            raise ValueError('P04 save requires exactly fourteen persisted properties')
        if any(type(v) is not int for v in payload.values()):raise ValueError('P04 save properties must be integers')
        candidate=State(**{name:payload[prop] for prop,name in PERSISTED_SIMPLE.items()})
        for name in ('Revision','Intro','Complete'):
            hi,lo=(payload['p04'+name+suffix] for suffix in ('Hi','Lo'))
            if not 0<=hi<BASE or not 0<=lo<BASE:raise ValueError('P04 serial limb is out of range')
            setattr(candidate,name.lower(),hi*BASE+lo)
        probe=P04()
        probe.state=candidate
        if not probe.validate():raise ValueError('Invalid P04 save state')
        self.state=candidate
        self.after_restore()
        return 1

    def snapshot(self):
        out=self.persisted()
        out.update(p04ContextValid=self.context_valid,p04Room=self.room,p04Apron=self.apron,p04Plan=self.plan,
                   p04Code=self.result.code,p04LineCount=len(self.result.lines),p04EventCount=len(self.result.events))
        out['p04ResultHi'],out['p04ResultLo']=divmod(self.result.revision,BASE)
        return out
