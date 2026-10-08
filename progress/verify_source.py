#!/usr/bin/env python3
"""Read-only exact inventory verification of this frozen WIP source edition."""
from pathlib import Path,PurePosixPath
import hashlib,json,os,stat,sys
ROOT=Path(__file__).resolve().parents[1]
MANIFEST='progress/manifests/SOURCE-FILES.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def safe(n):
 p=PurePosixPath(n)
 if not n or p.is_absolute() or p.as_posix()!=n or '..' in p.parts or '\\' in n:raise ValueError('Unsafe path: '+n)
 return p
def inventory():
 result={}
 for current,dirs,files in os.walk(ROOT,followlinks=False):
  if Path(current)==ROOT and '.git' in dirs:dirs.remove('.git')
  for d in dirs:
   if (Path(current)/d).is_symlink():raise ValueError('Directory symlink')
  for n in files:
   p=Path(current)/n;rel=str(p.relative_to(ROOT));safe(rel)
   if p.is_symlink() or not stat.S_ISREG(p.stat().st_mode):raise ValueError('Nonregular source file: '+rel)
   if rel!=MANIFEST:result[rel]={'sha256':sha(p),'bytes':p.stat().st_size,'mode':p.stat().st_mode&0o777}
 return dict(sorted(result.items()))
def main():
 if sys.flags.optimize:raise RuntimeError('Optimized Python is forbidden')
 saved=json.loads((ROOT/MANIFEST).read_text());actual=inventory()
 if saved['files']!=actual:
  expected=saved['files'];changed=sorted(n for n in set(actual)&set(expected) if actual[n]!=expected[n]);raise RuntimeError(json.dumps({'missing':sorted(set(expected)-set(actual)),'extra':sorted(set(actual)-set(expected)),'changed':changed}))
 maps={}
 for group in ('progress','late'):
  for name,component in json.loads((ROOT/group/'manifests/COMPONENTS.json').read_text()).items():maps[group+'/'+name]=component
 for name,component in maps.items():
  for n,row in component['files'].items():
   safe(n);safe(row['from']);p=ROOT/row['from']
   if {k:row[k] for k in ('sha256','bytes','mode')}!=actual[row['from']]:raise RuntimeError('Dependency mapping drift: '+name+'/'+n)
 print(json.dumps({'status':'PASS_FROZEN_WIP_SOURCE','files':len(actual)+1,'bytes':sum(r['bytes'] for r in actual.values())+(ROOT/MANIFEST).stat().st_size,'components':len(maps),'native_acceptance':False,'playable_release':False},sort_keys=True))
if __name__=='__main__':main()
