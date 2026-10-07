"""Narrow actual-source interpreter. Not native SCI, graphics, save or input proof."""
from pathlib import Path
import json,re,textwrap
HERE=Path(__file__).resolve().parents[1]
class Literal(str): pass
class Array(list): pass
class Pointer:
    def __init__(self,space,name):self.space=space;self.name=name
    def read(self):return self.space[self.name]
    def write(self,value):self.space[self.name]=value

def parse(text):
    tokens=[x for x in re.findall(r'"(?:\\.|[^"\\])*"|;[^\n]*|[()\[\]]|[^\s();\[\]]+',text) if not x.startswith(';')]
    def one(i):
        token=tokens[i]
        if token in ('(','['):
            out=Array() if token=='[' else [];end=']' if token=='[' else ')';i+=1
            while tokens[i]!=end:
                value,i=one(i);out.append(value)
            return out,i+1
        if token.startswith('"'):return Literal(json.loads(token)),i+1
        try:return int(token[1:],16) if token.startswith('$') else int(token),i+1
        except ValueError:return token,i+1
    out=[];i=0
    while i<len(tokens):v,i=one(i);out.append(v)
    return out
AST=[]
GAME=[]
PROP=[]
DEFAULTS={}
METHODS={}
LOCALS=[]
TEXT=[]

def measured(text,width):
    text=str(text)
    if not text:return 0,0
    cols=max(1,width//6)
    rows=[]
    # The packed font has a fixed 6px advance and 8px height. Explicit line
    # breaks and ordinary spaces follow the inspected SCI16 wrap boundary.
    for part in text.split('\n'):
        rows.extend(textwrap.wrap(part,cols,break_on_hyphens=False,replace_whitespace=False) or [''])
    return len(rows)*8,min(width,max(map(len,rows))*6)

class Return(Exception):
    def __init__(self,value):self.value=value
class VM:
    def __init__(self,stub_callbacks=True):
        self.p=DEFAULTS.copy();self.arrays={a[0]:[0]*a[1] for a in LOCALS}
        self.capacities={a[0]:a[1]*2 for a in LOCALS};self.calls=[];self.paint=[]
        self.stub_callbacks=stub_callbacks
    def pointer(self,name,e):
        name=name[1:];space=e if name in e else self.arrays
        return Pointer(space,name)
    def value(self,v):
        if isinstance(v,Pointer):
            result=v.read();return '' if isinstance(result,list) else result
        return v
    def write(self,pointer,value):
        if isinstance(value,str):
            cap=self.capacities.get(pointer.name)
            if cap is not None:assert len(value.encode('ascii'))+1<=cap,(pointer.name,len(value),cap)
        pointer.write(value)
    def call(self,name,*args):
        if self.stub_callbacks and name in {'uiHostAct','uiHostChoice','uiHostConfirm','uiHostMenu','uiHostSaveRequested','uiHostLoadRequested','uiHostClosed'}:
            self.calls.append((name,args));return 0
        method=METHODS[name];sig=method[1][1:]
        split=sig.index('&tmp') if '&tmp' in sig else len(sig)
        assert len(args)==split, ('arity mismatch',name,len(args),split)
        e=dict(zip(sig[:split],args))
        for n in sig[split+1:]:
            if isinstance(n,Array):e[n[0]]=[0]*n[1];self.capacities[n[0]]=n[1]*2
            else:e[n]=0
        try:
            value=0
            for n in method[2:]:value=self.ev(n,e)
            return value
        except Return as r:return r.value
    def ev(self,n,e):
        if isinstance(n,(int,Literal,Pointer)):return n
        if isinstance(n,Array):
            target=e.get(n[0],self.arrays.get(n[0]));index=self.ev(n[1],e)
            assert 0<=index<len(target),(n,index,len(target))
            return target[index]
        if isinstance(n,str):
            if n.startswith('@'):return self.pointer(n,e)
            if n in e:return e[n]
            if n in self.p:return self.p[n]
            if n=='self':return self
            raise ValueError(('unknown value',n))
        op,*a=n
        if op=='=':
            v=self.ev(a[1],e)
            if isinstance(a[0],Array):
                target=e.get(a[0][0],self.arrays.get(a[0][0]));index=self.ev(a[0][1],e)
                assert 0<=index<len(target),(a[0],index,len(target));target[index]=v
            else:(e if a[0] in e else self.p)[a[0]]=v
            return v
        if op in ('++','--'):return self.ev(['=',a[0],self.ev(a[0],e)+(1 if op=='++' else -1)],e)
        if op=='return':raise Return(self.ev(a[0],e) if a else 0)
        if op=='if':
            cut=a.index('else') if 'else' in a else len(a)
            branch=a[1:cut] if self.ev(a[0],e) else a[cut+1:];value=0
            for x in branch:value=self.ev(x,e)
            return value
        if op=='switch':
            value=self.ev(a[0],e)
            for branch in a[1:]:
                if branch[0]=='else' or self.ev(branch[0],e)==value:
                    result=0
                    for x in branch[1:]:result=self.ev(x,e)
                    return result
            return 0
        if op=='self':return self.call(a[0].rstrip(':'),*[self.ev(x,e) for x in a[1:]])
        if op=='not':return int(not self.ev(a[0],e))
        if op in ('and','or'):
            value=1 if op=='and' else 0
            for x in a:
                value=self.ev(x,e)
                if (op=='and' and not value) or (op=='or' and value):return value
            return value
        if op=='for':
            for x in a[0]:self.ev(x,e)
            count=0
            while self.ev(a[1],e):
                count+=1;assert count<1000
                for x in a[3:]:self.ev(x,e)
                for x in a[2]:self.ev(x,e)
            return 0
        if op=='while':
            count=0
            while self.ev(a[0],e):
                count+=1;assert count<1000
                for x in a[1:]:self.ev(x,e)
            return 0
        v=[self.ev(x,e) for x in a]
        if op=='TextSize':
            height,width=measured(self.value(v[1]),v[3]);self.write(v[0],[0,0,height,width]);return 0
        if op=='StrLen':return len(self.value(v[0]))
        if op=='StrCpy':self.write(v[0],str(self.value(v[1])));return v[0]
        if op=='GetFarText':self.write(v[2],TEXT[v[1]].decode('ascii'));return v[2]
        if op=='Format':
            self.write(v[0],str(self.value(v[1]))%tuple(self.value(x) for x in v[2:]));return v[0]
        if op=='Display':
            opts=v[1:];x=y=0;width=None;i=0
            while i<len(opts):
                code=opts[i];i+=1
                if code==100:x,y=opts[i:i+2];i+=2
                elif code==121:pass
                elif code==106:width=opts[i];i+=1
                else:i+=1
            assert width is not None and width>0,('Display width',v)
            text=self.value(v[0]);h,w=measured(text,width)
            self.paint.append(('text',x,y,x+w,y+h,text));return 0
        if op=='Graph':
            if v[0]==11:self.paint.append(('box',v[2],v[1],v[4],v[3],v[6]))
            return 0
        if op in ('SetPort','Palette','SetCursor','Wait','GetEvent'):return 0
        funcs={'+':lambda:sum(v),'-':lambda:v[0]-v[1],'*':lambda:v[0]*v[1],
               '/':lambda:v[0]//v[1],'mod':lambda:v[0]%v[1],
               '==':lambda:int(v[0]==v[1]),'!=':lambda:int(v[0]!=v[1]),
               '<':lambda:int(v[0]<v[1]),'>':lambda:int(v[0]>v[1]),
               '<=':lambda:int(v[0]<=v[1]),'>=':lambda:int(v[0]>=v[1]),
               '|':lambda:v[0]|v[1],'&':lambda:v[0]&v[1]}
        if op not in funcs:raise ValueError(('unsupported form',op))
        return funcs[op]()
    def key(self,key,mods=0):
        self.p.update(type=4,message=key,modifiers=mods)
        result=self.call('uiInput');self.call('uiBuildFocus');return result
    def click(self,x,y,mods=0):
        self.p.update(type=1,x=x,y=y,modifiers=mods)
        result=self.call('uiInput');self.call('uiBuildFocus');return result
    def controls(self):
        return [dict(index=i,action=self.arrays['uiActions'][i],payload=self.arrays['uiPayloads'][i],rect=tuple(self.arrays[n][i] for n in ['uiLefts','uiTops','uiRights','uiBottoms'])) for i in range(self.p['uiControlCount'])]
    def activate_action(self,action,payload=None):
        c=next(c for c in self.controls() if c['action']==action and (payload is None or c['payload']==payload))
        self.call('uiActivate',c['index']);self.call('uiBuildFocus')
