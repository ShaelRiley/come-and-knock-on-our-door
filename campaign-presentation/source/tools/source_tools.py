"""Balanced SCI method edits; strings and comments cannot spoof boundaries."""
import re
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|;[^\n]*|[()]|[^\s();]+')

def tokens(source):
    return [m for m in TOKEN.finditer(source) if not m.group().startswith(';')]

def spans(source, kind='method'):
    ts=tokens(source); result={}
    for i,t in enumerate(ts):
        if t.group()!='(' or i+3>=len(ts) or ts[i+1].group()!=kind: continue
        name=ts[i+3 if kind=='method' else i+2].group(); depth=0
        for q in ts[i:]:
            if q.group()=='(': depth+=1
            elif q.group()==')':
                depth-=1
                if depth==0: result[name]=(t.start(),q.end()); break
    return result

def methods(source):
    return {k:source[a:b] for k,(a,b) in spans(source).items()}

def replace_case(method,key,replacement):
    start=method.index('(switch location')+len('(switch location')
    ts=[t for t in tokens(method) if t.start()>=start]; depth=1
    for i,t in enumerate(ts):
        if t.group()=='(':
            if depth==1 and ts[i+1].group()==str(key):
                level=0
                for q in ts[i:]:
                    if q.group()=='(': level+=1
                    elif q.group()==')':
                        level-=1
                        if level==0:return method[:t.start()]+replacement+method[q.end():]
            depth+=1
        elif t.group()==')':depth-=1
    raise AssertionError(('missing location',key))

def merge_methods(source,new):
    old=methods(source)
    for name,(a,b) in sorted(spans(source).items(),key=lambda x:x[1][0],reverse=True):
        if name in new:source=source[:a]+new[name]+source[b:]
    extra='\n'.join(new[k] for k in new if k not in old)
    end=spans(source,'class')['Game'][1]-1
    return source[:end]+'\n'+extra+'\n'+source[end:]
