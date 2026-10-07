#!/usr/bin/env python3
"""Locate SCICompanion conditional-context leaks without editing sources."""
from pathlib import Path
import re, json, sys

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
ADAPTERS=['p04-domain-adapter','p05-domain-adapter','p06-domain-adapter','p07-domain-adapter','verbal-contest-adapter']
class Node(list):
    def __init__(self, start, kind): super().__init__(); self.start=start; self.kind=kind

def parse(source):
    tokens=[x for x in re.finditer(r'"(?:\\.|[^"\\])*"|;[^\n]*|[()\[\]]|[^\s();\[\]]+', source) if not x[0].startswith(';')]
    def one(i):
        token=tokens[i]
        if token[0] not in ('(', '['): return token[0],i+1
        node=Node(token.start(),token[0]); close=')' if token[0]=='(' else ']';i+=1
        while tokens[i][0]!=close:
            child,i=one(i);node.append(child)
        node.end=tokens[i].end()
        return node,i+1
    roots=[];i=0
    while i<len(tokens): node,i=one(i);roots.append(node)
    return roots

VALUE_OPS={'+','-','*','/','mod','==','!=','<','>','<=','>=','&','|','^','<<','>>','u<','u>','u<=','u>='}
RESETS={'not','~','++','--','=','+=','-=','*=','/=','mod=','&=','|=','^=','<<=','>>=','return','self','super'}

def audit(source):
    found=[];counts={};direct_call_arguments=[]
    def visit(n,method,cond=False,value_parent=None):
        if not isinstance(n,Node) or not n:return
        op=n[0]
        if n.kind=='[':
            for x in n[1:]:visit(x,method,False,None)
        elif op in ('method','procedure'):
            method=n[1][0]
            for x in n[2:]:visit(x,method)
        elif op=='if':
            visit(n[1],method,True,None)
            for x in n[2:]:visit(x,method,False,None)
        elif op in ('while','repeat'):
            visit(n[1],method,True,None)
            for x in n[2:]:visit(x,method,False,None)
        elif op=='for':
            for x in n[1]:visit(x,method,False,None)
            visit(n[2],method,True,None)
            for x in n[3]:visit(x,method,False,None)
            for x in n[4:]:visit(x,method,False,None)
        elif op=='switch':
            visit(n[1],method,False,None)
            for branch in n[2:]:
                for x in branch:visit(x,method,False,None)
        elif op in ('and','or'):
            counts[method]=counts.get(method,0)+1
            if cond and value_parent is not None:
                found.append(dict(method=method,line=source.count('\n',0,n.start)+1,start=n.start,end=n.end,
                    value_parent=value_parent,expression=source[n.start:n.end]))
            # The active port emits operand-valued short circuit when false;
            # unlike upstream _WriteFakeIfStatement it keeps false context.
            for x in n[1:]:visit(x,method,cond,None)
        elif isinstance(op,str) and op in VALUE_OPS:
            for x in n[1:]:visit(x,method,cond,op if cond else None)
        elif isinstance(op,str) and op in RESETS:
            if op in ('self','super'):
                for x in n[2:]:
                    if isinstance(x,Node) and x and x[0] in ('and','or','if'):
                        direct_call_arguments.append(dict(method=method,line=source.count('\n',0,x.start)+1,expression=source[x.start:x.end]))
            for x in n[1:]:visit(x,method,False,None)
        elif op in ('class','instance'):
            for x in n[2:]:visit(x,method,False,None)
        else:
            # Top-level declarations, method signatures and ordinary proc calls
            # never carry a surrounding conditional into their arguments.
            for x in n[1:]:visit(x,method,False,None)
    for root in parse(source):visit(root,'<top-level>')
    return dict(hazards=found,logical_count=sum(counts.values()),conditional_call_arguments=direct_call_arguments)

def value_sites(source):
    """Inventory unnormalized values for semantic review, not automatic errors."""
    found=[]
    def visit(n,method='<top-level>',parent=None):
        if not isinstance(n,Node) or not n:return
        if n[0]=='method':method=n[1][0]
        if n[0] in ('and','or') and parent is not None and parent[0] not in ('and','or','not','if','while','for'):
            found.append(dict(method=method,line=source.count('\n',0,n.start)+1,
                consumer=parent[0],expression=source[n.start:n.end]))
        for child in n:visit(child,method,n)
    for n in parse(source):visit(n)
    return found

def self_check():
    cases=[
        ('(method (x) (if (!= x (or a b)) (return 0)))',1),
        ('(method (x) (if (self f: (or a b)) (return 0)))',0),
        ('(method (x) (if (self f: (if (!= x (or a b)) 1 else 0)) (return 0)))',1),
        ('(method (x) (if (!= x (not (not (or a b)))) (return 0)))',0),
        ('(method (x) (= x (or (!= a (or b c)) d)))',0),
        ('(method (x) (if (< (+ 1 (and a b)) 2) (return 0)))',1),
    ]
    for source,count in cases:assert len(audit(source)['hazards'])==count,source

def main():
    self_check()
    result={}
    if len(sys.argv)>1:
        paths=[]
        for name in sys.argv[1:]:
            path=Path(name).resolve()
            paths.extend(sorted(path.glob('*.sc')) if path.is_dir() else [path])
    else:
        paths=[p for adapter in ADAPTERS for p in sorted((ROOT/'stock-sci'/adapter/'src').glob('*.sc*')) if p.suffix!='.sco']
    for path in paths:
        try:rel=str(path.relative_to(ROOT))
        except ValueError:rel=str(path)
        source=path.read_text();result[rel]=audit(source)
        result[rel]['unnormalized_value_sites_for_review']=value_sites(source)
    (OUT/('requested-inventory.json' if len(sys.argv)>1 else 'inventory.json')).write_text(json.dumps(result,indent=2)+'\n')
    for path,report in result.items():
        print(path,'logical=',report['logical_count'],'hazards=',len(report['hazards']),'conditional-call-args=',len(report['conditional_call_arguments']))
        for h in report['hazards']:print(' ',h['line'],h['method'],h['value_parent'],h['expression'])

if __name__=='__main__':main()
