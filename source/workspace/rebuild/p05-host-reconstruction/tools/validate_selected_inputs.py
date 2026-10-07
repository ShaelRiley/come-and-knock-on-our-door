from pathlib import Path
import hashlib,json,re

def require(ok,message):
 if not ok:raise RuntimeError(message)
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def check(root):
 H=Path(root)
 require(digest(H/'snapshot/domain/module985.sc')=='38a5bf402514511f24e74d25a445ee47716aab0552144b73724e7eb36a926cea','P05 domain authority changed')
 if (H/'CONTEST-INTEGRATION.json').exists():
  require(digest(H/'snapshot/contest/module986.sc')=='9dfbe07a0092eff89b0b919706d8e82a743b30ec9615906953e68fc85655bb81','Contest is not accepted r2')
  require(digest(H/'snapshot/contest/REVIEW-RESULT.json')=='236c2782a5dc5028c97043959c41f22345a1d1a6cee88f3d000ce5a9314b0ff6','Contest review changed')
  C=H/'snapshot/contest-scene';lock=C/'immutable-export-lock.json'
  require(digest(lock)=='229cb2411cab10348c15471beadb6108738fdb5d7cb7c0032fdd8a387f2fb830','Scene replacement lock missing')
  require(digest(C/'REVIEW-RESULT.json')=='9dd825e72d27bada066c6745b1ce23371004f42bbdefc5c2d0ca384a9b398f55','Scene independent review changed')
  data=json.loads(lock.read_text())
  for filename in ['module982.sc','route-map.json','route-tables.inc','230.text.bin','manifest.json','extension-contract.json']:
   p=C/filename;expected=data['files']['generated/'+filename]
   require(p.stat().st_size==expected['bytes'] and digest(p)==expected['sha256'],'Immutable scene import changed: '+filename)
  # Never accept a caller-provided manifest or compiled table as identity.
  # Verify the exact fixed alias boundary that independent review required.
  routes=json.loads((C/'route-map.json').read_text())['lookup']
  require(len(routes)==399,'Scene route extent changed')
  # All runtime unit descriptors are exact whole documents in reviewed source.
  tokens=[int(x) for x in re.findall(r'-?\d+', (C/'route-tables.inc').read_text().split('= [',1)[1].rsplit(']',1)[0])]
  require(len(tokens)==2793,'Scene table stride/extent changed')
  require(all(tokens[i+5]==0 for i in range(0,len(tokens),7)),'Windowed route slipped into full-unit contract')
 from validate_static_inputs import validate
 validate(H)
 return True
