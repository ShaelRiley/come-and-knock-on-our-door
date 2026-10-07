#!/usr/bin/env python3
"""Guarded additive source patch. Never replaces Main, resources or saves."""
from pathlib import Path
import argparse,hashlib,json,re,os
ROOT=Path(__file__).resolve().parent
TOKEN=re.compile(r'"(?:\\.|[^"\\])*"|;[^\n]*|[()]|[^\s();]+')
def method_spans(s):
 ts=[m for m in TOKEN.finditer(s) if not m.group().startswith(';')];out={}
 for i,t in enumerate(ts):
  if t.group()!='(' or i+3>=len(ts) or ts[i+1].group()!='method':continue
  name=ts[i+3].group();depth=0
  for q in ts[i:]:
   depth+=int(q.group()=='(')-int(q.group()==')')
   if depth==0:
    if name in out:raise ValueError('duplicate method '+name)
    out[name]=(t.start(),q.end());break
 return out
def transform(source,reverse=False):
 d=json.loads((ROOT/'APPROACH-DELTA.json').read_text());sp=method_spans(source)
 for name,sha in d['required_geometry_method_sha256'].items():
  if name not in sp:raise ValueError('missing geometry dependency '+name)
  a,b=sp[name]
  if hashlib.sha256(source[a:b].encode()).hexdigest()!=sha:raise ValueError('geometry dependency differs: '+name)
 a,b=sp[d['method']];old,new=d['before'],d['after']
 if reverse:old,new=new,old
 if source[a:b]!=old:raise ValueError('guarded hApproachX differs; independently review composition or already-applied delta')
 return source[:a]+new+source[b:]
def main():
 p=argparse.ArgumentParser();p.add_argument('module985',type=Path);p.add_argument('--reverse',action='store_true');p.add_argument('--check',action='store_true');args=p.parse_args()
 if args.module985.is_symlink():raise ValueError('refuse symlink target')
 old=args.module985.read_text();new=transform(old,args.reverse)
 if not args.check:
  tmp=args.module985.with_name(args.module985.name+'.approach-tmp');tmp.write_text(new);os.replace(tmp,args.module985)
 print('GUARD_CHECK_PASS' if args.check else 'PATCH_APPLIED',hashlib.sha256(old.encode()).hexdigest(),hashlib.sha256(new.encode()).hexdigest())
if __name__=='__main__':main()
