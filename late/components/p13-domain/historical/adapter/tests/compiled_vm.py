#!/usr/bin/env python3
"""Independent emitted SCI1.1 evaluator for P13 transition and validation regression.

Runs actual emitted instructions, local arrays, property writes and self sends.
Rejects unknown opcodes, array bounds and unbalanced stacks. No model/AST evaluation.
Derived from the earlier original compiled evaluator, extended for SCI load/store modes.
This is bytecode regression coverage, not native ScummVM acceptance.
"""
from pathlib import Path
import json, struct, re, sys, hashlib, operator

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
COMP=ROOT/'stock-sci/vendor/lucasartsifier/vendor/SCICompanion/SCICompanionLib/Src/Compile'
OPS={int(b):a for a,b in re.findall(r'^\s*(\w+)\s*=\s*(\d+)',(COMP/'PMachine.h').read_text(),re.M) if int(b)<128}
raw=(COMP/'PMachine.cpp').read_text().split('OpArgTypes_SCI0[TOTAL_OPCODES][3] = {')[1].split('};')[0]
ARGTYPES=[re.findall(r'ot\w+',x) for x in re.findall(r'\{([^}]+)\}',raw)]
def word(blob,offset):return struct.unpack_from('<H',blob,offset)[0]
def signed(value):return ((value+32768)&65535)-32768

BINARY={1:operator.add,2:operator.sub,3:operator.mul,4:lambda a,b:int(a/b),5:lambda a,b:a-int(a/b)*b,
 6:lambda a,b:(a&65535)>>b,7:operator.lshift,8:operator.xor,9:operator.and_,10:operator.or_,
 13:lambda a,b:int(a==b),14:lambda a,b:int(a!=b),15:lambda a,b:int(a>b),16:lambda a,b:int(a>=b),
 17:lambda a,b:int(a<b),18:lambda a,b:int(a<=b)}

class Compiled:
    def __init__(self, path, number, props):
        self.path=path;self.blob=(path/f'build/compiled/{number}.scr.bin').read_bytes()
        heap=(path/f'build/compiled/{number}.scr.bin.hep').read_bytes()
        selectors=json.loads((path/'selectors.json').read_text());self.rev={v:k for k,v in selectors.items()}
        obj=4+2*word(heap,2);methods=word(heap,obj+6);count=word(self.blob,methods)
        self.methods={self.rev[s]:p for s,p in [struct.unpack_from('<HH',self.blob,methods+2+i*4) for i in range(count)]}
        self.props={18+i*2:k for i,k in enumerate(props)};self.decoded={}
        self.trace=None; self.locals=[0]*word(heap,2); self.steps=0
    def inst(self,pc):
        if pc in self.decoded:return self.decoded[pc]
        raw=self.blob[pc];op=raw>>1;p=pc+1;args=[]
        for ty in ARGTYPES[op]:
            if ty=='otEMPTY':continue
            width=1 if ty=='otUINT8' or raw&1 else 2
            value=int.from_bytes(self.blob[p:p+width],'little');p+=width
            if ty in ('otLABEL','otINT') and value>=1<<(width*8-1):value-=1<<(width*8)
            args.append(value)
        result=(op,args,p);self.decoded[pc]=result;return result
    def execute(self,name,properties,params=(),strict=True):
        pc=self.methods[name];stack=[];acc=0;prev=0;temps=0;params=[len(params),*params]
        for tick in range(1000000):
            self.steps+=1
            op,args,end=self.inst(pc);arg=args[0] if args else None;nextpc=end;oldacc=acc
            if op==31:temps=arg;stack.extend([0]*arg)
            elif op==26:acc=arg
            elif op==27:stack.append(acc)
            elif op==28:stack.append(arg)
            elif op==29:stack.pop()
            elif op==30:stack.append(stack[-1])
            elif op==48:stack.append(prev)
            elif op==49:acc=properties[self.props[arg]]
            elif op==50:properties[self.props[arg]]=acc
            elif op==51:stack.append(properties[self.props[arg]])
            elif op==52:properties[self.props[arg]]=stack.pop()
            elif op in (53,54,55,56):
                prop=self.props[arg];properties[prop]=signed(properties[prop]+(1 if op in (53,55) else -1))
                if op in (53,54):acc=properties[prop]
                else:stack.append(properties[prop])
            elif op in (59,60,61):stack.append(op-59)
            elif op==24:
                if not acc:nextpc=end+arg
            elif op==23:
                if acc:nextpc=end+arg
            elif op==25:nextpc=end+arg
            elif op==12:acc=int(not acc)
            elif op==11:acc=-acc
            elif op==0:acc=~acc
            elif op in (1,2,3,4,5,6,7,8,9,10,13,14,15,16,17,18):
                left=stack.pop();right=acc
                acc=BINARY[op](left,right)
            elif 64<=op<=127:
                kind=op&3; index=arg+(acc if op&8 else 0)
                if kind==0:raise RuntimeError('Global access is outside isolated adapter')
                space={1:self.locals,2:stack,3:params}[kind]
                limit={1:len(self.locals),2:temps,3:len(params)}[kind]
                assert 0<=index<limit,('variable bounds',name,OPS[op],index,limit)
                mode=op&48; to_stack=bool(op&4)
                if mode==16:
                    # Indexed store consumes its value from the stack; acc is index.
                    value=stack.pop() if to_stack or op&8 else acc
                    space[index]=signed(value)
                else:
                    if mode in (32,48):space[index]=signed(space[index]+(1 if mode==32 else -1))
                    if to_stack:stack.append(space[index])
                    else:acc=space[index]
            elif op==42:
                count=arg//2;values=stack[-count:];del stack[-count:]
                selector,num,*par=values;assert num==len(par),(name,hex(pc),values)
                acc=self.execute(self.rev[selector],properties,par,strict)
            elif op==36:
                # Every P13 return must have exactly its declared temporary frame.
                permitted={temps}
                if strict:assert len(stack) in permitted,('stack imbalance',name,hex(pc),stack,temps)
                if self.trace is not None:self.trace.append((name,hex(pc),'RET',acc,list(stack)))
                return acc
            else:raise RuntimeError(('unsupported opcode',name,hex(pc),OPS.get(op),args))
            acc=signed(acc)
            if self.trace is not None:self.trace.append((name,hex(pc),OPS[op],args,acc,list(stack),hex(nextpc)))
            prev=oldacc;pc=nextpc
        raise RuntimeError(('instruction budget',name))
