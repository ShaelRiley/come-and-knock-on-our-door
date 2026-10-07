"""Accepted P08 caption helpers, unchanged, with explicit font0 metrics."""
from pathlib import Path
import importlib.util,struct
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('accepted_p08_caption',H/'inputs/p08/generate.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
sha,dump,norm,paginate,source_segments=base.sha,base.dump,base.norm,base.paginate,base.source_segments
SPEAKERS,talk=base.SPEAKERS,base.talk
def font_metrics():
 raw=(H/'inputs/p08/inputs/resources/000.font.bin').read_bytes()
 count,height=struct.unpack_from('<HH',raw,2)
 assert height==8 and count>=128
 for code in range(32,127):
  pos=struct.unpack_from('<H',raw,6+code*2)[0]
  assert raw[pos:pos+2]==bytes((6,8))
 return dict(resource=0,sha256=sha(raw),glyphs=count,width=6,height=8)
