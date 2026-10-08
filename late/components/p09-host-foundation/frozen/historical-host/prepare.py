"""Whole selector/class universe package, preserving prior non-class resources."""
from pathlib import Path
import argparse,hashlib,json,re,struct,sys,shutil
H=Path(__file__).resolve().parent;S=H.parent;B=S/'campaign-p08-courtyard-candidate';sys.path.insert(0,str(S));import pack
p=argparse.ArgumentParser();p.add_argument('mode',choices=['seed','package']);mode=p.parse_args().mode
v=(B/'build/game/resource.000').read_bytes();assert hashlib.sha256(v).hexdigest()=='8fe1e92ec7a0f48ee42a8977852b8ebc1f3205ea526352cfd0b9e29c7526a98d'
m=json.loads((B/'build/game/manifest.json').read_text());res={(r['type'],r['number']):v[r['offset']+9:r['offset']+9+r['size']] for r in m['resources'] if r['type'] not in (2,17) and (r['type'],r['number']) not in ((6,996),(6,997))}
assert (3,210) not in res;res[3,210]=(H/'generated/210.text.bin').read_bytes()
A=S.parent/'assets/art-candidates/conservatory-p09-props-r1'
art_pins={'243-p09-tags-card-r1.view.bin':'e45ffb9bfc5758d0f86e098584f8921d343de754caba99d8c2ca9813170afadc','manifest.json':'073fa18fef7469d9daebbb004ad2a665f6e55218c662c8b0aaff1b3d526529f4','geometry-contract.json':'90a7d5acb8cf2e5e125189c4ef10e96ef3ff5b4e5cbd954d2c7097993c94a0aa'}
for name,digest in art_pins.items():assert hashlib.sha256((A/name).read_bytes()).hexdigest()==digest,('changed P09 art',name)
assert (0,243) not in res;res[0,243]=(A/'243-p09-tags-card-r1.view.bin').read_bytes()
(H/'snapshot/p09-art-inputs.json').write_text(json.dumps({str(A/n):v for n,v in art_pins.items()},indent=2)+'\n')

b=json.loads((B/'selectors.json').read_text());pack.SELECTORS.clear();pack.SELECTORS.update(b)
source='\n'.join(p.read_text() for p in sorted((H/'src').glob('*.sc')));props=[]
for body in re.findall(r'\(properties\s*([^()]*)\)',source,re.S):props.extend(re.sub(r';[^\n]*','',body).split()[::2])
names=sorted(set(props+re.findall(r'\(method \((\w+)',source))-set(b))
for i,n in enumerate(names,max(v for v in b.values() if v<4096)+1):assert i<4096;pack.SELECTORS[n]=i
assert all(pack.SELECTORS[k]==v for k,v in b.items());res[6,997]=pack.selector_resource();res[6,996]=b''.join(struct.pack('<HH',0,n) for n in [0,0,*range(980,992)])
out=H/'build/game' if mode=='package' else H
if mode=='package':
 budgets=[]
 for n in (0,*range(980,992),997):
  p=H/f'build/compiled/{n}.scr.bin';s=p.read_bytes();heap=Path(str(p)+'.hep').read_bytes();size=((len(s)+3)//4)*4+len(heap);assert size<=65535,(n,size)
  res[2,n]=s;res[17,n]=heap;budgets.append(dict(script=n,script_bytes=len(s),heap_bytes=len(heap),combined_with_alignment=size,headroom=65535-size))
 (H/'evidence/segment-budgets.json').write_text(json.dumps(budgets,indent=2)+'\n')
pack.pack_resources(res,out);pack.validate_resources(out)
if mode=='package':
 for folder in (B/'build/game',S/'p09-scene-data/generated/speech'):
  for p in folder.iterdir():
   if p.name[:1] in '@#':assert not (out/p.name).exists() or (out/p.name).read_bytes()==p.read_bytes();shutil.copy2(p,out/p.name)
(H/'selectors.json').write_text(json.dumps(pack.SELECTORS,indent=2)+'\n')
(H/'evidence/selector-delta.json').write_text(json.dumps(dict(preserved=len(b),added={n:pack.SELECTORS[n] for n in names}),indent=2)+'\n')
print('Packaged',len(res),'resources;',len(names),'new selectors')
