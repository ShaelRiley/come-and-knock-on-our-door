"""Reconstructed narrow SCI source executor derived from durable P02 primitives.
Operand-valued logical expressions and 16-bit arithmetic. No native claim.
"""
from pathlib import Path
import re,json
class Literal(str):pass
class Array(list):pass
class Returned(Exception):
    def __init__(self,value):self.value=value

def parse(text):
    tokens=[s for s in re.findall(r'"(?:\\.|[^"\\])*"|;[^\n]*|[()\[\]]|[^\s();\[\]]+',text) if not s.startswith(';')]
    def one(i):
        t=tokens[i]
        if t in ('(','['):
            out=Array() if t=='[' else [];end=']' if t=='[' else ')';i+=1
            while tokens[i]!=end:
                v,i=one(i);out.append(v)
            return out,i+1
        if t.startswith('"'):return Literal(json.loads(t)),i+1
        try:return int(t[1:],16) if t.startswith('$') else int(t),i+1
        except ValueError:return t,i+1
    result=[];i=0
    while i<len(tokens):v,i=one(i);result.append(v)
    return result

def word(n):return ((n+32768)&65535)-32768
class VM:
    def __init__(self,path=None,classname='P08State'):
        path=path or Path(__file__).resolve().parents[1]/'src/module989.sc'
        ast=parse(Path(path).read_text());cl=next(n for n in ast if n[:2]==['class',classname]);props=next(n[1:] for n in cl[2:] if n[0]=='properties')
        assert len(props)%2==0
        self.p=dict(zip(props[::2],props[1::2]));self.methods={n[1][0]:n for n in cl[2:] if n[0]=='method'}
        self.constants={n[1]:n[2] for n in ast if n[0]=='define'}
        self.arrays={a[0]:[0]*a[1] for n in ast if n[0]=='local' for a in n[1:]}
        self.call('p08Init')
    def call(self,name,*args):
        method=self.methods[name];sig=method[1][1:];split=sig.index('&tmp') if '&tmp' in sig else len(sig)
        assert len(args)==split,(name,args,sig)
        env=dict(zip(sig[:split],args))
        for v in sig[split+1:]:
            if isinstance(v,Array):env[v[0]]=[0]*v[1]
            else:env[v]=0
        try:
            result=0
            for n in method[2:]:result=self.ev(n,env)
            return result
        except Returned as r:return r.value
    def ev(self,n,e):
        if isinstance(n,(int,Literal)):return n
        if isinstance(n,Array):
            i=self.ev(n[1],e);a=e.get(n[0],self.arrays.get(n[0]));assert 0<=i<len(a),(n,i)
            return a[i]
        if isinstance(n,str):
            if n=='self':return self
            if n in e:return e[n]
            if n in self.p:return self.p[n]
            if n in self.constants:return self.constants[n]
            raise ValueError(('unknown value',n))
        op,*a=n
        if op=='=':
            key,v=a;value=self.ev(v,e)
            if isinstance(key,Array):
                i=self.ev(key[1],e);arr=e.get(key[0],self.arrays.get(key[0]));assert 0<=i<len(arr),(key,i);arr[i]=value
            else:
                assert key in e or key in self.p,key
                (e if key in e else self.p)[key]=value
            return value
        if op in ('++','--'):return self.ev(['=',a[0],word(self.ev(a[0],e)+(1 if op=='++' else -1))],e)
        if op=='return':raise Returned(self.ev(a[0],e) if a else 0)
        if op=='if':
            cut=a.index('else') if 'else' in a else len(a);branch=a[1:cut] if self.ev(a[0],e) else a[cut+1:];value=0
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
        if op=='self' or (type(op) is str and op in e and hasattr(e[op],'call')):
            target=self if op=='self' else e[op];i=0;result=0
            while i<len(a):
                selector=a[i];i+=1;args=[]
                while i<len(a) and not (type(a[i]) is str and a[i].endswith((':','?'))):args.append(self.ev(a[i],e));i+=1
                name=selector[:-1]
                if selector.endswith('?'):assert not args;result=target.p[name]
                elif name in target.p:
                    assert len(args)==1;target.p[name]=args[0];result=args[0]
                else:result=target.call(name,*args)
            return result
        if op=='not':return int(not self.ev(a[0],e))
        if op in ('and','or'):
            value=1 if op=='and' else 0
            for x in a:
                value=self.ev(x,e)
                if op=='and' and not value or op=='or' and value:return value
            return value
        if op=='for':
            for x in a[0]:self.ev(x,e)
            count=0
            while self.ev(a[1],e):
                count+=1;assert count<=5000
                for x in a[3:]:self.ev(x,e)
                for x in a[2]:self.ev(x,e)
            return 0
        v=[self.ev(x,e) for x in a]
        funcs={'+':lambda:sum(v),'-':lambda:v[0]-sum(v[1:]),'*':lambda:v[0]*v[1],'/':lambda:int(v[0]/v[1]),'mod':lambda:v[0]-int(v[0]/v[1])*v[1],'==':lambda:int(v[0]==v[1]),'!=':lambda:int(v[0]!=v[1]),'<':lambda:int(v[0]<v[1]),'>':lambda:int(v[0]>v[1]),'<=':lambda:int(v[0]<=v[1]),'>=':lambda:int(v[0]>=v[1]),'&':lambda:v[0]&v[1],'|':lambda:v[0]|v[1]}
        if op not in funcs:raise ValueError(('unsupported form',op))
        return word(funcs[op]())
