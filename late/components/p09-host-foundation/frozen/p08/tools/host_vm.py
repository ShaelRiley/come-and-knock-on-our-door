#!/usr/bin/env python3
"""Bounded actual SCI1.1 bytecode runner with typed, deterministic kernel mocks.

This is a test oracle, not ScummVM. Loads only freshly compiled module resources.
No source expression evaluation, bytecode substitution, GUI, sound or native save.
"""
from pathlib import Path
from dataclasses import dataclass
from collections.abc import MutableSequence
from collections import Counter
import copy,hashlib,json,math,os,re,struct,sys,textwrap
from extract_sci11 import extract
HERE=Path(__file__).resolve().parents[1]
DEFAULT=Path(os.environ.get('CAKOOD_CHECKPOINT',str(HERE.parent/'p03-editable-checkpoint'))).resolve()
DEFAULT_BUILD=Path(os.environ.get('CAKOOD_BUILD',str(HERE/'build/fresh'))).resolve()
class VMError(RuntimeError):pass
class EndOfEvents(Exception):pass
def signed(x):return ((x+32768)&65535)-32768
def normalize(x):return signed(x) if isinstance(x,int) else x
def require(ok,*why):
    if not ok:raise VMError(why)
@dataclass(eq=False)
class Region:
    name:str
    words:list|None=None
    data:bytes|None=None
    initialized:set|None=None
    allocations:tuple=()
    def limit(self,p):
        for start,size in self.allocations:
            if start<=p<start+size:return start+size
        return self.size()
    def size(self):return len(self.data) if self.data is not None else 2*len(self.words)
    def byte(self,p):
        require(0<=p<self.size(),'Byte read bounds',self.name,p,self.size())
        if self.data is not None:return self.data[p]
        require(self.initialized is None or p//2 in self.initialized,'Uninitialized byte read',self.name,p)
        v=self.words[p//2];require(isinstance(v,int),'Pointer read as bytes',self.name,p,v)
        return (v&65535)>>((p%2)*8)&255
    def put(self,p,v):
        require(self.words is not None and 0<=p<self.size(),'Byte write bounds/read-only',self.name,p,self.size())
        old=self.words[p//2];require(isinstance(old,int),'Pointer overwrite as bytes',self.name,p)
        shift=p%2*8;self.words[p//2]=signed((old&~(255<<shift))|(v<<shift))
        if self.initialized is not None:self.initialized.add(p//2)
@dataclass(frozen=True)
class Pointer:
    region:Region
    offset:int
    def __repr__(self):return f'<{self.region.name}+{self.offset}>'
class ArrayView(MutableSequence):
    def __init__(self,region,start,count):self.region=region;self.start=start;self.length=count
    def __len__(self):return self.length
    def __iter__(self):return iter(self.region.words[self.start:self.start+self.length])
    def __getitem__(self,i):
        if isinstance(i,slice):return list(self)[i]
        if i<0:i+=self.length
        require(0<=i<self.length,'Array index',i,self.length);return self.region.words[self.start+i]
    def __setitem__(self,i,v):
        if isinstance(i,slice):
            ids=range(*i.indices(self.length));require(len(ids)==len(v),'Array slice length')
            for j,x in zip(ids,v):self[j]=x
        else:
            if i<0:i+=self.length
            require(0<=i<self.length,'Array store',i,self.length);self.region.words[self.start+i]=normalize(v)
    def __delitem__(self,i):raise VMError('Fixed-size SCI array')
    def insert(self,i,v):raise VMError('Fixed-size SCI array')
    def __repr__(self):return repr(list(self))
    def __eq__(self,o):return list(self)==o
    def __contains__(self,v):return v in self.text() if isinstance(v,str) else v in list(self)
    def text(self):return read_string(Pointer(self.region,self.start*2))
    def __str__(self):return self.text()
def read_string(p):
    require(isinstance(p,Pointer),'String pointer required',p);out=bytearray()
    for i in range(p.offset,p.region.limit(p.offset)):
        c=p.region.byte(i)
        if not c:return out.decode('latin1')
        out.append(c)
    raise VMError(('Unterminated string',p))
def write_string(p,value):
    require(isinstance(p,Pointer),'Writable pointer required',p);data=value.encode('latin1')+b'\0'
    require(p.offset+len(data)<=p.region.limit(p.offset),'String buffer overflow',p,len(data),p.region.limit(p.offset))
    for i,c in enumerate(data):p.region.put(p.offset+i,c)
    return p
class Module:
    def __init__(self,vm,number):
        self.number=number;self.vm=vm;self.blob=(vm.build/f'compiled/{number}.scr.bin').read_bytes();self.heap=(vm.build/f'compiled/{number}.scr.bin.hep').read_bytes()
        self.layout=extract(vm.build/f'compiled/{number}.scr.bin',vm.build/f'compiled/{number}.scr.bin.hep',vm.selector_path)
        self.local=Region(f'locals:{number}',[signed(v) for v in self.layout['locals']],allocations=tuple((a['word_offset']*2,a['word_count']*2) for a in vm.abi['modules'].get(str(number),{}).get('locals',[])));self.heapregion=Region(f'heap:{number}',data=self.heap)
        self.objects={};self.decoded={};self.relocations=set(self.layout['script_relocations'])
    def pointer(self,offset):
        if offset in self.objects:return self.objects[offset]
        require(self.layout['strings_start']<=offset<len(self.heap),'Invalid LOFS heap pointer',self.number,offset)
        return Pointer(self.heapregion,offset)
class Object:
    def __init__(self,vm,module,data):
        self.vm=vm;self.module=module;self.name=data['name'];self.offset=data['heap_offset'];self.is_class=data['is_class'];self.species=data['species'];self.superclass=data['superclass']
        self.p={p['selector']:p['signed_value'] for p in data['properties'] if p['index']>=9}
        self.propmap={p['index']*2:p['selector'] for p in data['properties'] if p['index']>=9}
        self.methods={m['selector']:m['code_offset'] for m in data['methods']};self.draws=[]
    def __repr__(self):return f'<{self.module.number}:{self.name}>'
    @property
    def arrays(self):return self.vm.arrays(self.module.number)
    def call(self,name,*args):return self.vm.call(self,name,args)
class HostVM:
    def __init__(self,checkpoint=DEFAULT,build=DEFAULT_BUILD,budget=2000000):
        require(not sys.flags.optimize,'Optimized Python disables scenario assertions; run without -O/-OO')
        self.checkpoint=Path(checkpoint);self.build=Path(build);self.budget=budget;self.steps=0;self.depth=0
        receipt=json.loads((self.build/'compile-receipt.json').read_text());require(receipt['status']=='PASS_FRESH_COMPILE','Missing fresh compile receipt')
        for row in receipt['modules']:
            n=row['module']
            for part,path in [('script',self.build/f'compiled/{n}.scr.bin'),('heap',self.build/f'compiled/{n}.scr.bin.hep')]:require(hashlib.sha256(path.read_bytes()).hexdigest()==row[f'{part}_sha256'],'Fresh output hash changed',n,part)
        self.abi=json.loads((self.checkpoint/'source-provenance/ABI-MAPPINGS.json').read_text());self.names={s['selector_id']:s['name'] for s in self.abi['selectors']}
        self.selector_path=self.build/'selector-list.json'
        selector_override=os.environ.get('CAKOOD_SELECTORS')
        selector_list=json.loads(Path(selector_override).read_text()) if selector_override else self.abi['selectors']
        if isinstance(selector_list,dict):selector_list=[{'selector_id':v,'name':k} for k,v in selector_list.items()]
        self.names={s['selector_id']:s['name'] for s in selector_list}
        require(json.loads(self.selector_path.read_text())==selector_list,'Existing selector metadata differs from bound ABI/override')
        table=json.loads((HERE/'reference/opcode-tables.json').read_text());self.opnames={int(k):v for k,v in table['opcodes'].items()};self.argtypes=table['argtypes']
        self.knames={int(k):v for k,v in json.loads((HERE/'reference/kernels.json').read_text()).items()}
        self.modules={};self.objects={};self.classes={};self.executed=Counter();self.calls=Counter();self.kernel_calls=Counter();self.kernel_attempts=Counter();self.packets=[];self.returns=[];self.ktrace=[];self.paint=[];self.trace=None;self.now=0;self.audio_position=-1;self.audio_gain=100;self.draw_success=True
        for n in sorted(r['module'] for r in receipt['modules']):
            m=Module(self,n);self.modules[n]=m
            for data in m.layout['objects']:
                o=Object(self,m,data);m.objects[o.offset]=o;self.objects[o.name]=o
                if o.is_class:self.classes[o.species]=o
        for o in self.objects.values():
            if not o.is_class:
                require(o.superclass in self.classes,'Instance class missing',o)
                o.propmap=dict(self.classes[o.superclass].propmap)
                o.p={name:signed(struct.unpack_from('<H',o.module.heap,o.offset+offset)[0]) for offset,name in o.propmap.items()}
        for m in self.modules.values():
            for p in m.layout['heap_relocations']:
                if 4<=p<4+2*len(m.local.words):m.local.words[(p-4)//2]=m.pointer(struct.unpack_from('<H',m.heap,p)[0])
        self.resources={}
        for e in json.loads((self.checkpoint/'reference/resources.json').read_text()):
            if e['type'] in (3,7,0):self.resources[e['type'],e['number']]=(self.checkpoint/'assets/resources'/Path(e['extracted_path']).name).read_bytes()
        self.event_queue=None;self.frame_tick=6;self.frames=0;self.chain=[];self.files={};self.handles={};self.next_handle=1
    def arrays(self,n):return {a['name']:ArrayView(self.modules[n].local,a['word_offset'],a['word_count']) for a in self.abi['modules'].get(str(n),{}).get('locals',[])}
    def decode(self,m,pc):
        if pc in m.decoded:return m.decoded[pc]
        require(0<=pc<len(m.blob),'PC bounds',m.number,pc);raw=m.blob[pc];op=raw>>1;p=pc+1;args=[]
        for kind in self.argtypes[op]:
            if kind=='otEMPTY':continue
            require(kind!='otDEBUGSTRING','Unsupported debug operand')
            width=1 if kind in ('otUINT8','otINT8') else 2 if kind in ('otUINT16','otINT16') else 1 if raw&1 else 2
            require(p+width<=len(m.blob),'Truncated instruction',m.number,pc)
            value=int.from_bytes(m.blob[p:p+width],'little');p+=width
            if kind in ('otLABEL','otINT','otINT8','otINT16') and value>=1<<(width*8-1):value-=1<<(width*8)
            args.append(value)
        m.decoded[pc]=(op,args,p);return op,args,p
    def method_boundaries(self,m,entry):
        if not hasattr(m,'boundary_cache'):m.boundary_cache={}
        if entry not in m.boundary_cache:
            starts=sorted({method['code_offset'] for obj in m.layout['objects'] for method in obj['methods']})
            require(entry in starts,'Unknown method entry',m.number,entry)
            index=starts.index(entry);limit=starts[index+1] if index+1<len(starts) else m.layout['script_relocation_offset']
            allowed=set();pc=entry
            while pc<limit:
                allowed.add(pc);_,_,pc=self.decode(m,pc);require(pc<=limit,'Instruction crosses method boundary',m.number,entry,pc,limit)
            m.boundary_cache[entry]=allowed
        return m.boundary_cache[entry]
    def resolve(self,obj,name):
        require(isinstance(obj,Object),'Send target is not object',obj,name)
        seen=set();cur=obj
        while cur:
            if name in cur.methods:return cur.module,cur.methods[name]
            require(cur not in seen,'Class inheritance loop',obj);seen.add(cur)
            cur=self.classes.get(cur.superclass)
        raise VMError(('Unknown method',obj,name))
    def send(self,obj,packet):
        require(isinstance(obj,Object),'Send target is not object',obj);i=0;result=0
        while i<len(packet):
            require(i+2<=len(packet),'Truncated send header',obj,packet);sel,argc=packet[i:i+2];i+=2
            require(isinstance(sel,int) and sel in self.names,'Unknown selector',sel);name=self.names[sel]
            require(isinstance(argc,int) and 0<=argc<=len(packet)-i,'Send argument count',obj,name,argc,packet)
            args=packet[i:i+argc];i+=argc;self.packets.append((obj.name,name,argc))
            if name in obj.p:
                require(argc<=1,'Property arity',obj,name,argc)
                if argc:obj.p[name]=normalize(args[0])
                result=obj.p[name]
            else:result=self.call(obj,name,args)
        require(i==len(packet),'Send trailing data',packet);return result
    def call(self,obj,name,args=()):
        m,pc=self.resolve(obj,name);require(self.depth<100,'Call depth',obj,name)
        self.depth+=1;self.calls[m.number,name]+=1;self.chain.append((obj.name,name));self.steps_at_entry=self.steps
        try:return self.execute(obj,m,name,pc,args)
        except VMError as e:
            if not getattr(e,'chain',None):e.chain=list(self.chain);e.args=(*e.args,{'chain':e.chain[-16:]})
            raise
        finally:self.depth-=1;self.chain.pop()
    def execute(self,obj,m,name,pc,args):
        allowed=self.method_boundaries(m,pc)
        stack=[];acc=0;prev=0;temps=Region(f'temp:{m.number}:{name}',[],initialized=set());params=Region(f'param:{m.number}:{name}',[len(args),*[normalize(v) for v in args]]);linked=False
        def pop():require(stack,'Operand stack underflow',obj,name,hex(pc));return stack.pop()
        def packet(bytes_,argc_word=False):
            require(bytes_%2==0,'Odd call/send byte count',obj,name,pc,bytes_);count=bytes_//2+int(argc_word)
            require(0<count<=len(stack),'Call/send stack bounds',obj,name,pc,count,len(stack))
            values=stack[-count:];del stack[-count:]
            if argc_word:require(values[0]==count-1,'Call argc does not match emitted bytes',obj,name,pc,values[0],count-1)
            return values
        def space(scope):return [self.modules[0].local,m.local,temps,params][scope]
        while True:
            require(pc in allowed,'PC outside method instruction boundaries',obj,name,pc)
            self.steps+=1;require(self.steps<=self.budget,'Instruction budget exceeded',self.budget)
            op,oper,end=self.decode(m,pc);arg=oper[0] if oper else None;nxt=end;self.executed[op]+=1
            if self.trace is not None:self.trace.append((m.number,name,pc,self.opnames.get(op),oper,acc,list(stack)))
            if op==31:
                require(not linked and not stack,'Unexpected LINK',obj,name,pc);linked=True;temps.words=[0]*arg
            elif op==26:acc=signed(arg)
            elif op==27:stack.append(acc)
            elif op==28:stack.append(signed(arg))
            elif op==29:pop()
            elif op==30:v=pop();stack.extend([v,v])
            elif op in (59,60,61):stack.append(op-59)
            elif op==62:stack.append(obj)
            elif op==46:acc=obj
            elif op==48:stack.append(prev)
            elif op in (23,24,25):
                if op==25 or (bool(acc) if op==23 else not acc):nxt=end+arg
            elif op==12:acc=int(not acc)
            elif op in (0,11):
                require(isinstance(acc,int),'Unary numeric operand',op,acc);acc=~acc if op==0 else -acc
            elif op in range(1,11) or op in range(13,23):
                left=pop();right=acc
                if op>=13:prev=right
                if op in (13,14):acc=int((left==right) if op==13 else (left!=right))
                else:
                    require(isinstance(left,int) and isinstance(right,int),'Numeric operands required',self.opnames[op],left,right)
                    if op==1:acc=left+right
                    elif op==2:acc=left-right
                    elif op==3:acc=left*right
                    elif op in (4,5):
                        require(right!=0,'Division by zero',obj,name,pc);q=(abs(left)//abs(right))*(-1 if (left<0)!=(right<0) else 1);acc=q if op==4 else left-q*right
                    elif op==6:require(0<=right<16,'Shift count',right);acc=(left&65535)>>right
                    elif op==7:require(0<=right<16,'Shift count',right);acc=left<<right
                    elif op==8:acc=left^right
                    elif op==9:acc=left&right
                    elif op==10:acc=left|right
                    elif op==15:acc=int(left>right)
                    elif op==16:acc=int(left>=right)
                    elif op==17:acc=int(left<right)
                    elif op==18:acc=int(left<=right)
                    elif op==19:acc=int((left&65535)>(right&65535))
                    elif op==20:acc=int((left&65535)>=(right&65535))
                    elif op==21:acc=int((left&65535)<(right&65535))
                    elif op==22:acc=int((left&65535)<=(right&65535))
            elif 49<=op<=56:
                require(arg in obj.propmap,'Property offset',obj,arg);prop=obj.propmap[arg]
                if op==49:acc=obj.p[prop]
                elif op==50:obj.p[prop]=acc
                elif op==51:stack.append(obj.p[prop])
                elif op==52:obj.p[prop]=pop()
                else:
                    require(isinstance(obj.p[prop],int),'Increment pointer property',prop)
                    obj.p[prop]=signed(obj.p[prop]+(1 if op in (53,55) else -1))
                    if op in (53,54):acc=obj.p[prop]
                    else:stack.append(obj.p[prop])
            elif op in (37,42):
                target=obj if op==42 else acc;acc=self.send(target,packet(arg))
            elif op==40:
                require(arg in self.classes,'Unknown class',arg);acc=self.classes[arg]
            elif op==45:
                scope=(arg>>1)&3;index=oper[1]+(acc if arg&0x10 else 0);r=space(scope)
                require(isinstance(index,int) and 0<=index<len(r.words),'LEA bounds',scope,index,len(r.words));acc=Pointer(r,2*index)
            elif op in (57,58):
                require(pc+1 in m.relocations,'Missing LOFS relocation',m.number,pc);v=m.pointer(arg)
                if op==57:acc=v
                else:stack.append(v)
            elif op==33:
                values=packet(oper[1],True);self._kernel_accumulator=acc;acc=self.kernel(arg,values[1:])
            elif op>=64:
                r=space(op&3);index=arg+(acc if op&8 else 0)
                require(isinstance(index,int) and 0<=index<len(r.words),'Variable bounds',obj,name,hex(pc),self.opnames[op],index,len(r.words))
                family=(op-64)//16;tos=bool(op&4)
                if family in (0,2,3):require(r.initialized is None or index in r.initialized,'Uninitialized variable',obj,name,index)
                if family==0:
                    if tos:stack.append(r.words[index])
                    else:acc=r.words[index]
                elif family==1:
                    r.words[index]=normalize(pop() if tos or op&8 else acc)
                    if r.initialized is not None:r.initialized.add(index)
                else:
                    require(isinstance(r.words[index],int),'Increment pointer variable',index);r.words[index]=signed(r.words[index]+(1 if family==2 else -1))
                    if tos:stack.append(r.words[index])
                    else:acc=r.words[index]
            elif op==36:
                # SCI RET discards the frame. Switch early returns legitimately
                # leave deciding values here; they never spill into caller stack.
                self.returns.append((m.number,name,pc,len(temps.words),tuple(stack)));return normalize(acc)
            else:
                self.executed[op]-=1
                if not self.executed[op]:del self.executed[op]
                raise VMError(('Unsupported opcode',m.number,name,hex(pc),self.opnames.get(op,op),oper))
            acc=normalize(acc);pc=nxt
    def kernel(self,k,args):
        name=self.knames.get(k,f'unknown:{k}');self.kernel_attempts[name]+=1
        result=self._kernel(k,args);self.kernel_calls[name]+=1;return result
    def _kernel(self,k,args):
        name=self.knames.get(k,f'unknown:{k}');self.ktrace.append((name,tuple(args)))
        def arity(*ns):require(len(args) in ns,'Kernel arity',name,len(args),ns)
        if name=='ScriptID':
            arity(1,2);n=args[0];idx=args[1] if len(args)==2 else 0;require(n in self.modules,'Unknown script',n);m=self.modules[n];require(0<=idx<len(m.layout['exports']),'Export bounds',n,idx);return m.pointer(m.layout['exports'][idx])
        if name=='GetFarText':
            arity(3);res,entry,dest=args;require((3,res) in self.resources,'Missing text resource',res);entries=self.resources[3,res].split(b'\0');require(0<=entry<len(entries)-1,'Text entry bounds',res,entry);return write_string(dest,entries[entry].decode('latin1'))
        if name in ('StrLen','StrEnd'):
            arity(1);n=len(read_string(args[0]));return n if name=='StrLen' else Pointer(args[0].region,args[0].offset+n)
        if name in ('StrCpy','StrCat'):
            arity(2);dest,src=args;return write_string(dest,(read_string(dest) if name=='StrCat' else '')+read_string(src))
        if name=='Format':
            require(len(args)>=2,'Format arity');dest,fmt,*vals=args;fmt=read_string(fmt);types=re.findall(r'%(?:\d+)?([dsxX])',fmt);require(len(types)==len(vals),'Format arguments',fmt,vals)
            vals=[read_string(v) if t=='s' else v for t,v in zip(types,vals)];return write_string(dest,fmt%tuple(vals))
        if name=='TextSize':
            arity(4);dest,ptr,font,width=args;require(font==0 and width>0,'Unsupported font/width',font,width);text=read_string(ptr)
            require((7,font) in self.resources,'Missing font resource',font)
            fontblob=self.resources[7,font];count=struct.unpack_from('<H',fontblob,2)[0]
            require(struct.unpack_from('<H',fontblob,4)[0]==8,'Unsupported font height')
            for char in set(text)-set('\n\r'):
                code=ord(char) if ord(char)<count else ord('?');offset=struct.unpack_from('<H',fontblob,6+code*2)[0]
                require(fontblob[offset:offset+2]==bytes((6,8)),'Unsupported variable glyph metrics',font,code)
            # Verified bundled 6x8 glyph advances; simplified word wrapping, no pixel proof.
            rows=[]
            for line in text.split('\n'):rows.extend(textwrap.wrap(line,width=max(1,width//6),break_long_words=True,break_on_hyphens=False) or [''])
            vals=[0,0,len(rows)*8,min(width,max(map(len,rows),default=0)*6)]
            require(isinstance(dest,Pointer) and dest.offset%2==0 and dest.region.words is not None,'TextSize destination',dest)
            start=dest.offset//2;require(dest.offset+8<=dest.region.limit(dest.offset),'TextSize bounds',dest);dest.region.words[start:start+4]=vals
            if dest.region.initialized is not None:dest.region.initialized.update(range(start,start+4))
            return 0
        if name in ('Graph','Display','DrawCel','SetPort','Palette'):
            if name=='Graph':require(args and ((args[0]==11 and len(args)==9) or (args[0]==12 and len(args)==6)),'Unsupported Graph operation',args)
            if name=='SetPort':arity(6)
            if name=='Palette':require(args==[1,999,2],'Unsupported Palette operation',args)
            if name=='DrawCel':arity(7,8);self.objects['cakood'].draws.append(tuple(args))
            if name=='Display':require(args and isinstance(args[0],Pointer),'Display text pointer',args);self.paint.append(read_string(args[0]))
            if name=='Graph' and args[0]==12:require(self.draw_success,'Mock Graph12 presentation failure')
            self.ktrace[-1]=(name,tuple(args));return getattr(self,'_kernel_accumulator',0) if name=='Graph' else 1
        if name=='GetEvent':
            arity(2);require(args[0]==32767 and isinstance(args[1],Object),'Unsupported GetEvent arguments',args)
            require(self.event_queue is not None,'Event queue not explicitly configured')
            if not self.event_queue:raise EndOfEvents()
            event=self.event_queue.pop(0);require(set(event)<=set(('type','message','modifiers','x','y')),'Unexpected event fields',event)
            target=args[1]
            for field in ('type','message','modifiers'):target.p[field]=signed(event.get(field,0))
            for field in ('x','y'):
                if field in event:target.p[field]=signed(event[field])
            self.now=signed(self.now+self.frame_tick);self.frames+=1;return int(bool(target.p['type']))
        if name=='Wait':arity(1);require(args[0]==1,'Unsupported mock wait',args);return 0
        if name=='GetTime':arity(0,1);return self.now
        if name=='DoAudio':
            require(args,'DoAudio suboperation');sub=args[0]
            if sub==3:arity(1);self.audio_position=-1;return 0
            if sub==6:arity(1);return self.audio_position
            if sub==8:arity(2);self.audio_gain=args[1];return self.audio_gain
            if sub==2:arity(6);self.audio_position=0;return 1
            raise VMError(('Unsupported DoAudio operation',args))
        if name=='DoSync':
            require(args,'DoSync suboperation');sub=args[0]
            if sub==2:arity(1);return 0
            if sub==0:arity(7);return 1
            if sub==1:arity(2);require(isinstance(args[1],Object),'DoSync target');args[1].p.update(syncTime=-1,syncCue=-1);return 0
            raise VMError(('Unsupported DoSync operation',args))
        if name=='DoSound':
            require(args and args[0] in (0,1,2,3,4,5,6,7,8,10,12,13,14,15,17),'Unsupported DoSound operation',args)
            require(1<=len(args)<=4,'DoSound arity',args);return 0
        if name=='FileIO':
            require(args,'FileIO suboperation');sub=args[0]
            if sub in (0,10):
                arity(3 if sub==0 else 2);path=read_string(args[1]);require(re.fullmatch(r'(?:speech|p01audio|p02state)\d{4,5}\.csv',path),'Unapproved mocked file path',path)
                if sub==10:return int(path in self.files)
                require(args[2]==2,'Unsupported mock file open mode',args[2]);handle=self.next_handle;self.next_handle+=1;self.handles[handle]=path;self.files[path]='';return handle
            if sub in (1,6):
                arity(2 if sub==1 else 3);require(args[1] in self.handles,'Unknown mock file handle',args[1])
                if sub==6:self.files[self.handles[args[1]]]+=read_string(args[2])
                else:del self.handles[args[1]]
                return 1
            raise VMError(('Unsupported FileIO operation',args))
        if name=='Abs':arity(1);return signed(abs(args[0]))
        if name=='Sqrt':arity(1);require(args[0]>=0,'Negative sqrt');return math.isqrt(args[0])
        if name=='IsObject':arity(1);return int(isinstance(args[0],Object))
        raise VMError(('Unsupported kernel',name,args))
    def report(self):
        return {'instructions':self.steps,'opcode_count':len(self.executed),'opcodes':{self.opnames[k]:v for k,v in sorted(self.executed.items())},'method_count':len(self.calls),'methods':{f'{m}:{n}':v for (m,n),v in sorted(self.calls.items())},'kernels':dict(self.kernel_calls),'kernel_attempts':dict(self.kernel_attempts),'send_packets':len(self.packets),'boundaries':['Graph/Display/DrawCel traces only; no pixel/native proof','TextSize deterministic bundled 6x8 metrics','DoAudio/DoSync/DoSound deterministic mocks; no audible/PCM timing acceptance','Explicit deterministic clock; no wall time scheduling','Object/local snapshot is harness serialization, never a native SCI save']}
    def snapshot(self):
        """Portable JSON state of persistent objects and locals, not a SCI save."""
        regions={id(m.local):(n,'local') for n,m in self.modules.items()}
        regions.update({id(m.heapregion):(n,'heap') for n,m in self.modules.items()})
        def enc(v):
            if isinstance(v,int):return v
            if isinstance(v,Object):return {'object':[v.module.number,v.name]}
            if isinstance(v,Pointer):
                require(id(v.region) in regions,'Transient pointer escaped into persistent state',v)
                n,kind=regions[id(v.region)];return {'pointer':[n,kind,v.offset]}
            raise VMError(('Unsupported snapshot value',v))
        receipt=json.loads((self.build/'compile-receipt.json').read_text())
        identity={str(r['module']):[r['script_sha256'],r['heap_sha256']] for r in receipt['modules']}
        return {'format':'cakood-bounded-host-state-v1','program':identity,'objects':{name:{k:enc(v) for k,v in o.p.items()} for name,o in self.objects.items()},'locals':{str(n):[enc(v) for v in m.local.words] for n,m in self.modules.items()}}
    def restore(self,state):
        """Restore only matching compiled program identities; mocks start silent."""
        require(state.get('format')=='cakood-bounded-host-state-v1','Unknown snapshot format')
        require(state.get('program')==self.snapshot()['program'],'Snapshot compiled program identity mismatch')
        require(set(state.get('objects',{}))==set(self.objects),'Snapshot object set mismatch')
        require(set(state.get('locals',{}))==set(map(str,self.modules)),'Snapshot local segment set mismatch')
        def dec(v):
            if type(v) is int:require(-32768<=v<=32767,'Snapshot word range',v);return v
            require(isinstance(v,dict) and len(v)==1,'Snapshot typed value malformed',v)
            if 'object' in v:
                n,name=v['object'];require(name in self.objects and self.objects[name].module.number==n,'Snapshot object reference',v);return self.objects[name]
            if 'pointer' in v:
                n,kind,off=v['pointer'];require(n in self.modules and kind in ('heap','local'),'Snapshot pointer segment',v)
                region=self.modules[n].heapregion if kind=='heap' else self.modules[n].local;require(type(off) is int and 0<=off<region.size(),'Snapshot pointer bounds',v);return Pointer(region,off)
            raise VMError(('Snapshot unknown typed value',v))
        new_props={};new_locals={}
        for name,props in state['objects'].items():
            require(set(props)==set(self.objects[name].p),'Snapshot property set mismatch',name);new_props[name]={k:dec(v) for k,v in props.items()}
        for n,values in state['locals'].items():
            require(len(values)==len(self.modules[int(n)].local.words),'Snapshot locals length',n);new_locals[int(n)]=[dec(v) for v in values]
        for name,props in new_props.items():self.objects[name].p=props
        for n,values in new_locals.items():self.modules[n].local.words[:]=values
        self.audio_position=-1;self.audio_gain=0;self.now=0;return self.objects['cakood']
    def pump(self,events,tick=6):
        """Execute the actual eventLoop until its explicit mock input queue ends.

        Queue exhaustion is an intentional harness yield at the next GetEvent,
        after all prior frames, Graph12 calls and receipt hooks ran in bytecode.
        It is not game exit and does not inject quitRequested or bypass methods.
        """
        require(self.depth==0 and self.event_queue is None,'Nested event pump')
        require(type(tick) is int and 0<=tick<=12,'Invalid mock tick delta',tick)
        self.event_queue=list(events);self.frame_tick=tick;before=self.frames
        try:self.objects['cakood'].call('eventLoop')
        except EndOfEvents:pass
        finally:self.event_queue=None
        return self.frames-before
