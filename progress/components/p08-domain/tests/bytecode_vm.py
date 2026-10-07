"""Reconstructed fail-closed numeric SCI1.1 bytecode oracle for new script986.
Runs fresh compiler-produced instructions; mocks optional host callbacks.
It is not ScummVM and makes no native/audio/save compatibility claim.
"""
from pathlib import Path
import sys,json
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H/'tools'))
from resource_decode import layout,selectors,decode,instruction_tables,words,signed
from source_vm import word,parse
ROOT=H.parent
R=H/'reference'
TABLES=json.loads((R/'opcode-tables.json').read_text())
OPS={int(k):v for k,v in TABLES['opcodes'].items()}
ARGTYPES=TABLES['argtypes']
class BytecodeVM:
    def __init__(self,script=None,heap=None,names=None):
        self.blob=Path(script or H/'build/compiled/989.scr.bin').read_bytes();hb=Path(heap or H/'build/compiled/989.scr.bin.hep').read_bytes()
        self.names=selectors(names or H/'selectors.json');self.ops,self.argtypes=OPS,ARGTYPES
        data=layout(self.blob,hb,self.names);cl=data['objects'][0];ob=data['objects'][1]
        self.p={k:v for k,v in ob['properties'].items() if not k.startswith('-') and k!='name'}
        self.methods=cl['methods'];self.propmap=cl['property_offsets'];self.locals=[signed(x) for x in data['local_values']];self.executed=0;self.decoded={}
        self.array_ranges={};offset=0
        for key,size in json.loads((H/'manifest.json').read_text())['arrays'].items():
            self.array_ranges[key]=(offset,size);offset+=size
        ast=parse((H/'src/module989.sc').read_text());cls=next(n for n in ast if n[:2]==['class','P08State'])
        def switch_count(n):return (int(bool(n) and n[0]=='switch')+sum(switch_count(x) for x in n if isinstance(x,list))) if isinstance(n,list) else 0
        self.switches={m[1][0]:switch_count(m) for m in cls[2:] if m[0]=='method'}
        self.arities={m[1][0]:(m[1][1:].index('&tmp') if '&tmp' in m[1] else len(m[1])-1) for m in cls[2:] if m[0]=='method'}
        self.max_stack=0;self.max_depth=0;self.depth=0;self.call('p08Init')
    @property
    def arrays(self):return {k:self.locals[i:i+n] for k,(i,n) in self.array_ranges.items()}
    def send(self,target,values):
        result=0;i=0
        while i<len(values):
            selector,count=values[i:i+2];i+=2;params=values[i:i+count];i+=count;name=self.names[selector]
            assert len(params)==count,(name,count,params)
            if name in target.p:
                assert count<=1,(name,count)
                if count:target.p[name]=params[0]
                result=target.p[name]
            else:result=target.call(name,*params)
        assert i==len(values)
        return result
    def call(self,name,*params):
        assert len(params)==self.arities[name],('arity mismatch',name,params,self.arities[name])
        self.depth+=1;self.max_depth=max(self.max_depth,self.depth)
        pc=self.methods[name];stack=[];acc=0;prev=0;temps=[];par=[len(params),*params];steps=0
        def pop():
            assert stack,('stack underflow',name,hex(pc));return stack.pop()
        while steps<100000:
            steps+=1;self.executed+=1;self.max_stack=max(self.max_stack,len(stack))
            if pc not in self.decoded:self.decoded[pc]=decode(self.blob,pc,self.argtypes)
            op,args,end=self.decoded[pc];arg=args[0] if args else None;nextpc=end
            if op==31:temps=[0]*arg
            elif op==26:acc=signed(arg)
            elif op==27:stack.append(acc)
            elif op==28:stack.append(signed(arg))
            elif op==29:pop()
            elif op==30:stack.append(stack[-1])
            elif op in (59,60,61):stack.append(op-59)
            elif op==62:stack.append(self)
            elif op==46:acc=self
            elif op==48:stack.append(prev)
            elif op==24:
                if not acc:nextpc=end+arg
            elif op==23:
                if acc:nextpc=end+arg
            elif op==25:nextpc=end+arg
            elif op==12:acc=int(not acc)
            elif op==11:acc=word(-acc)
            elif op==0:acc=word(~acc)
            elif op in range(1,11) or op in range(13,23):
                l=pop();r=acc
                if op>=13:prev=r
                if op==1:acc=l+r
                elif op==2:acc=l-r
                elif op==3:acc=l*r
                elif op==4:acc=int(l/r)
                elif op==5:acc=l-int(l/r)*r
                elif op==6:acc=(l&65535)>>r
                elif op==7:acc=l<<r
                elif op==8:acc=l^r
                elif op==9:acc=l&r
                elif op==10:acc=l|r
                elif op==13:acc=int(l==r)
                elif op==14:acc=int(l!=r)
                elif op==15:acc=int(l>r)
                elif op==16:acc=int(l>=r)
                elif op==17:acc=int(l<r)
                elif op==18:acc=int(l<=r)
                elif op==19:acc=int((l&65535)>(r&65535))
                elif op==20:acc=int((l&65535)>=(r&65535))
                elif op==21:acc=int((l&65535)<(r&65535))
                elif op==22:acc=int((l&65535)<=(r&65535))
                acc=word(acc)
            elif op in range(49,57):
                key=self.propmap[arg]
                if op==49:acc=self.p[key]
                elif op==50:self.p[key]=acc
                elif op==51:stack.append(self.p[key])
                elif op==52:self.p[key]=pop()
                else:
                    self.p[key]=word(self.p[key]+(1 if op in (53,55) else -1))
                    if op in (53,54):acc=self.p[key]
                    else:stack.append(self.p[key])
            elif op in (42,37):
                count=arg//2;assert count<=len(stack),(name,pc,count,stack)
                vals=stack[-count:];del stack[-count:]
                target=self if op==42 else acc
                acc=self.send(target,vals)
            elif op>=64:
                scope=op&3;assert scope!=0,('global access unsupported',name,pc)
                space={1:self.locals,2:temps,3:par}[scope];idx=arg+(acc if op&8 else 0)
                assert 0<=idx<len(space),(name,hex(pc),self.ops[op],idx,len(space))
                family=(op-64)//16;tos=bool(op&4)
                if family==0:
                    value=space[idx]
                    if tos:stack.append(value)
                    else:acc=value
                elif family==1:
                    # Indexed accumulator stores take value from stack; acc is index.
                    value=pop() if tos or op&8 else acc;space[idx]=value
                else:
                    space[idx]=word(space[idx]+(1 if family==2 else -1))
                    if tos:stack.append(space[idx])
                    else:acc=space[idx]
            elif op==36:
                # SCI RET destroys the current frame, including live switch deciding words.
                # Same permitted bound as static gate; no tail allowed outside switch methods.
                assert len(stack)<=self.switches[name],('return stack imbalance',name,hex(pc),stack,params)
                self.depth-=1
                return acc
            else:raise ValueError(('unsupported bytecode',name,hex(pc),self.ops.get(op),args))
            pc=nextpc
        raise RuntimeError(('runaway',name,pc))
