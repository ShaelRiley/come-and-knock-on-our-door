"""Wire unchanged accepted source evaluator to the current static integrity domain."""
from pathlib import Path
import sys
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H/'tools'))
from scene_vm import VM as BaseVM
from resource_codec import decode
def VM(path,classname,resources=None):
 path=Path(path)
 if classname!='SceneDialogue':return BaseVM(path,classname,resources)
 prior=path.name=='module982-input.sc' or path.is_relative_to(H/'inputs')
 src=H/('inputs/src' if prior else 'generated/src')
 game=H/'inputs/native-game';allres=decode((game/'resource.map').read_bytes(),(game/'resource.000').read_bytes());res={n:v.split(b'\0')[:-1] for (t,n),v in allres.items() if t==3}
 if resources:res.update(resources)
 if not prior:
  for p in list((H/'generated').glob('*.text.bin'))+list((H/'generated/static').glob('*.text.bin')):res[int(p.name.split('.')[0])]=p.read_bytes().split(b'\0')[:-1]
 s=BaseVM(path,classname,res);g=BaseVM(src/'module985.sc','P05State',res);a=BaseVM(src/'module981.sc','MusicTransport',res)
 for vm in [s,g,a]:vm.objects.update(script982=s,script985=g,script981=a)
 return s
